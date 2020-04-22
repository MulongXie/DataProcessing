import cv2
import json
import numpy as np
from random import randint as rint
import os
from os.path import join as pjoin


def rm_repeated_objects(node, gap):
    def obj_is_same(obj_a, obj_b, gap):
        if obj_a['class'] != obj_b['class']:
            return False
        if abs(obj_a['bounds'][0] - obj_b['bounds'][0]) < gap and \
                abs(obj_a['bounds'][1] - obj_b['bounds'][1]) < gap and \
                abs(obj_a['bounds'][2] - obj_b['bounds'][2]) < gap and \
                abs(obj_a['bounds'][3] - obj_b['bounds'][3]) < gap:
            return True
        return False

    if 'children' not in node:
        return node
    children = node['children']
    children_new = []
    children_grand = []

    for child in children:
        children_new.append(rm_repeated_objects(child, gap))

    repeat = np.full(len(children_new), False)
    for i in range(len(children_new)):
        if obj_is_same(node, children_new[i], gap):
            if 'children' in children_new[i]:
                children_grand += children_new[i]['children']
            repeat[i] = True
            continue

        if repeat[i]: continue

        for j in range(i + 1, len(children_new)):
            if obj_is_same(children_new[i], children_new[j], gap):
                if 'children' in children_new[j]:
                    if 'children' in children_new[i]:
                        children_new[i]['children'] += children_new[j]['children']
                    else:
                        children_new[i]['children'] = children_new[j]['children']
                repeat[j] = True

    children_non_redundant = []
    for i in range(len(repeat)):
        if not repeat[i]:
            children_non_redundant.append(children_new[i])
    node['children'] = children_non_redundant + children_grand
    return node


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))


def draw_node(node, board, count, layer, shrink_ratio=4):
    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, -1)
    cv2.putText(board, node['class'], (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
    print(node['class'])
    cv2.imshow('board', shrink(board, shrink_ratio))
    cv2.waitKey()
    count += 1
    if 'children' not in node:
        return count
    for child in node['children']:
        count = draw_node(child, board, count, layer+1)
    return count


if '__main__':
    save = False
    show = True
    start = 0  # start point
    end = 1000
    input_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\'
    output_root = 'E:\\Temp\\rico-tree'
    for index in range(start, end):
        img_path = input_root + 'all\\' + str(index) + '.jpg'
        json_path = input_root + 'simplified\\' + str(index) + '.json'
        if os.path.exists(img_path):
            print(img_path)
            img = cv2.imread(img_path)
            objs = json.load(open(json_path, encoding="utf8"))
            if objs is not None:
                objs = rm_repeated_objects(objs, 5)
                if show:
                    org = cv2.resize(img, (1440, 2560))
                    board = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
                    cv2.imshow('org', shrink(org, 4))
                    count = draw_node(objs, board, 0, 0)
                if save:
                    joutput = open(pjoin(output_root, str(index) + '.json'), 'w')
                    json.dump(objs, joutput, indent=4)

        index += 1
        if index > end:
            break
