import cv2
import json
import numpy as np
from random import randint as rint
import os
from os.path import join as pjoin
import pandas as pd


def check_class_and_size(node, compos_select):
    # filter by size
    if node['bounds'][2] - node['bounds'][0] < 10 or node['bounds'][3] - node['bounds'][1] < 10:
        node['class'] = 'invalid'
    # filter by class
    else:
        cat = compos_select[compos_select['class_name'] == node['class']]['category'].values
        if len(cat) == 0:
            node['class'] = 'invalid'
        else:
            node['class'] = cat[0]

    if 'children' in node:
        for i, child in enumerate(node['children']):
            check_class_and_size(child, compos_select)


def rm_invalid_nodes(node):
    if 'children' not in node:
        return

    children_new = []
    for child in node['children']:
        rm_invalid_nodes(child)
        if child['class'] == 'invalid':
            if 'children' in child:
                children_new += child['children']
        else:
            children_new.append(child)
    node['children'] = children_new


def prune_tree(tree, compos_select):
    check_class_and_size(tree, compos_select)
    rm_invalid_nodes(tree)


def rm_repeated_objects(node, gap):
    def obj_is_same(obj_a, obj_b, gap):
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
        # if identical with parent node, ignore this child
        if obj_is_same(node, children_new[i], gap):
            if 'children' in children_new[i]:
                children_grand += children_new[i]['children']
            repeat[i] = True
            continue
        if repeat[i]: continue

        for j in range(i + 1, len(children_new)):
            # if identical with previous non-layout child, ignore this one
            if obj_is_same(children_new[i], children_new[j], gap):
                if 'Layout' not in children_new[i]['class']:
                    delete = j
                    remain = i
                else:
                    delete = i
                    remain = j
                if 'children' in children_new[delete]:
                    if 'children' in children_new[remain]:
                        children_new[remain]['children'] += children_new[delete]['children']
                    else:
                        children_new[remain]['children'] = children_new[delete]['children']
                repeat[j] = True

    children_non_redundant = []
    for i in range(len(repeat)):
        if not repeat[i] and children_new[i] is not None:
            children_non_redundant.append(children_new[i])
    node['children'] = children_non_redundant + children_grand
    return node


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))


def draw_node(node, board, layer, shrink_ratio=4):
    if node is None:
        return
    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, -1)
    cv2.putText(board, node['class'], (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
    print(node['class'])
    cv2.imshow('board', shrink(board, shrink_ratio))
    cv2.waitKey()
    if 'children' in node:
        for child in node['children']:
            draw_node(child, board, layer+1)


def main():
    save = True
    show = False
    start = 487  # start point
    end = 100000
    none_tree = 0

    compos_select = pd.read_csv('rico_class_widget_layout.csv', index_col=0)
    input_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\'
    output_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-tree-filtered\\widget-layout\\'
    for index in range(start, end):
        img_path = input_root + 'all\\' + str(index) + '.jpg'
        json_path = input_root + 'simplified\\' + str(index) + '.json'
        if os.path.exists(img_path) and os.path.exists(json_path):
            print(json_path)
            ui_tree = json.load(open(json_path, encoding="utf8"))
            if ui_tree is not None:
                prune_tree(ui_tree, compos_select)

                ui_tree = rm_repeated_objects(ui_tree, 5)
                if ui_tree is None:
                    none_tree += 1
                    print('*** Tree is None: %d %s ***' % (none_tree, img_path))
                    show = True

                if show:
                    img = cv2.imread(img_path)
                    org = cv2.resize(img, (1440, 2560))
                    board = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
                    cv2.imshow('org', shrink(org, 4))
                    draw_node(ui_tree, board, 0)
                if save:
                    joutput = open(pjoin(output_root, str(index) + '.json'), 'w')
                    json.dump(ui_tree, joutput, indent=4)

        index += 1
        if index > end:
            break


if '__main__':
   main()