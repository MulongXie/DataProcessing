import json
import cv2
from os.path import join as pjoin
import os


def view_blocks(blocks, org):
    for block in blocks['blocks']:
        cv2.rectangle(org, (block['column_min'], block['row_min']),
                      (block['column_max'], block['row_max']), (0,255,0), 3)
    cv2.imshow('blocks', cv2.resize(org, (int(org.shape[1] / org.shape[0] * 500), 500)))
    cv2.waitKey()


if __name__ == '__main__':
    show = True
    start = 0  # start point
    end = 100000
    img_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\all'
    block_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-block-json'

    for index in range(start, end):
        img_path = pjoin(img_root, str(index) + '.jpg')
        block_path = pjoin(block_root, str(index) + '.json')
        if not os.path.exists(block_path):
            continue
        print('View:', block_path)

        blocks_json = json.load(open(block_path))
        img = cv2.imread(img_path)
        img = cv2.resize(img, (int(img.shape[1] / img.shape[0] * 800), 800))
        view_blocks(blocks_json, img)
