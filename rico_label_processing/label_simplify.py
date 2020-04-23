import cv2
import json
import numpy as np
from random import randint as rint
import os
from os.path import join as pjoin


def simplify_objects(root):
    def iter_kids(obj):
        if obj['bounds'][2] - obj['bounds'][0] == 0 or obj['bounds'][3] - obj['bounds'][1] == 0:
            return
        extracted_obj = {'class':obj['class'], 'bounds':[int(b) for b in obj['bounds']]}
        if 'children' in obj and len(obj['children']) > 0:
            extracted_obj['children'] = []
            children = obj['children']
            for child in children:
                if child is None:
                    continue
                kids = iter_kids(child)
                if kids is not None:
                    extracted_obj['children'].append(kids)
        return extracted_obj

    if 'activity' in root:
        root = root['activity']['root']
    objects = iter_kids(root)
    return objects


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
    end = 100000
    input_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\all\\'
    output_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\simplified\\'
    for index in range(start, end):
        img_path = input_root + str(index) + '.jpg'
        json_path = input_root + str(index) + '.json'
        if os.path.exists(img_path):
            print(img_path)
            # extract Ui components, relabel them
            img = cv2.imread(img_path)
            jfile = json.load(open(json_path, encoding="utf8"))
            objs = simplify_objects(jfile)
            if objs is not None:
                if show:
                    org = cv2.resize(img, (1440, 2560))
                    board = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
                    cv2.imshow('org', shrink(org, 4))
                    count = draw_node(objs, board, 0, 0)
                    cv2.imshow('all_labels', board)
                    cv2.waitKey()
                    print(count)
                if save:
                    joutput = open(pjoin(output_root, str(index) + '.json'), 'w')
                    # joutput = open('sb.json', 'w')
                    json.dump(objs, joutput, indent=4)

        index += 1
        if index > end:
            break
