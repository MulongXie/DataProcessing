import cv2
import json
import numpy as np
from random import randint as rint
import os
from os.path import join as pjoin


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))


def draw_node(node, board, layer, shrink_ratio=4, show_node=True):

    color = (rint(0, 255), rint(0, 255), rint(0, 255))
    label = node['componentLabel'] if 'componentLabel' in node else node['class']
    cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, -1)
    cv2.putText(board, label, (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    if show_node:
        print(node['class'])
        cv2.imshow('board', shrink(board, shrink_ratio))
        cv2.waitKey()

    if 'children' not in node:
        return
    for child in node['children']:
         draw_node(child, board, layer+1)
    return


if '__main__':
    start = 0  # start point
    end = 100000
    image_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\all\\'
    # label_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\simplified\\'
    label_root = 'E:\\Mulong\\Datasets\\gui\\rico\\semantic_annotations\\'
    for index in range(start, end):
        img_path = image_root + str(index) + '.jpg'
        json_path = label_root + str(index) + '.json'
        if os.path.exists(img_path) and os.path.exists(json_path):
            print(img_path)
            # extract Ui components, relabel them
            img = cv2.imread(img_path)
            tree = json.load(open(json_path, encoding="utf8"))
            if 'activity' in tree:
                tree = tree['activity']['root']
            if tree is not None:
                org = cv2.resize(img, (1440, 2560))
                board = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
                cv2.imshow('org', shrink(org, 4))
                draw_node(tree, board, 0)
                cv2.imshow('board', shrink(board, 4))
                cv2.waitKey()

        index += 1
        if index > end:
            break
