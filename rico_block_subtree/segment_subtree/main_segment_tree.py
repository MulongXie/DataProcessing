import cv2
import json
import numpy as np
import os
import time

import segment_subtree.Detected_Block as Block
import segment_subtree.Tree as Tree
import lib_ip.ip_draw as draw
import lib_ip.ip_preprocessing as pre
from lib_ip.Bbox import Bbox


def shrink(img, ratio):
    return cv2.resize(img, (int(img.shape[1] / ratio), int(img.shape[0] / ratio)))


def resize_block(blocks, det_height, tgt_height, bias):
    for block in blocks:
        block.resize_bbox(det_height, tgt_height, bias)


def check_subtree(block, tree, org, test=False):
    '''
    check if the tree can be segmented by block
    relation: -1 : block in tree
               0  : block, tree are not intersected
               1  : tree in block
               2  : block, tree are intersected
               3  : block and tree are same
    '''
    relation = block.relation(tree['bounds'])
    if test:
        print(relation, block.put_bbox(), tree['bounds'])
        img = org.copy()
        board_test_blk = draw.draw_bounding_box(img, [block], line=5)
        board_test_tree = cv2.resize(img, (1440, 2560))
        Tree.draw_tree(tree, board_test_tree)
        cv2.imshow('tree-test', cv2.resize(board_test_tree, (300, 500)))
        cv2.imshow('blk-test', cv2.resize(board_test_blk, (300, 500)))
        cv2.waitKey()

    # block contains tree or block and tree are same
    if relation == 1 or relation == 3:
        return [tree]
    # non-intersected
    elif relation == 0:
        return None
    # intersected or tree contains block, search children
    else:
        if 'children' not in tree:
            return None
        subtrees = []
        for child in tree['children']:
            subtree = check_subtree(block, child, org)
            if subtree is not None:
                if type(subtree) is list:
                    subtrees += subtree
        if len(subtrees) > 0:
            return subtrees
        else:
            return None


def segment_subtree(blocks, tree, org):
    segmented_subtree = {'segments':[]}
    for block in blocks:
        subtree = check_subtree(block, tree, org)
        if subtree is not None:
            segment = {'block': block.put_bbox(), 'subtree':subtree}
            segmented_subtree['segments'].append(segment)
    return segmented_subtree


def main():
    save = True
    show = False
    bad_num = 0
    none_tree = 0
    num = 0
    start = 19558  # start point
    end = 100000
    img_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\all\\'
    block_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-block\\json\\'
    tree_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-tree-filtered\\widget-layout\\'
    subtree_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-subtree\\widget-layout\\'
    for index in range(start, end):
        img_path = img_root + str(index) + '.jpg'
        block_path = block_root + str(index) + '.json'
        tree_path = tree_root + str(index) + '.json'
        subtree_path = subtree_root + str(index) + '.json'

        if not os.path.exists(block_path) or not os.path.exists(tree_path):
            continue

        start_time = time.clock()
        img, _ = pre.read_img(img_path, resize_height=2560)

        blocks = Block.load_blocks(block_path)
        resize_block(blocks, det_height=800, tgt_height=2560, bias=0)
        board_block = draw.draw_bounding_box(img, blocks, line=5)

        try:
            tree = Tree.load_tree(tree_path)
        except:
            bad_num += 1
            print('*** Fuck Json: %d %s ***' % (bad_num, tree_path))
            continue
        if tree is not None:
            segments = segment_subtree(blocks, tree, img)
        else:
            none_tree += 1
            print('*** Tree is None: %d %s ***' % (none_tree, tree_path))
            continue

        if show:
            board_tree = np.full((2560, 1440, 3), 255, dtype=np.uint8)  # used for draw new labels
            Tree.draw_tree(tree, board_tree, 0)
            cv2.imshow('block', cv2.resize(board_block, (300, 500)))
            cv2.imshow('tree', cv2.resize(board_tree, (300, 500)))
            cv2.waitKey()
            cv2.destroyAllWindows()
            Tree.view_segments(segments, img)

        if save:
            jfile = open(subtree_path, 'w')
            json.dump(segments, jfile, indent=4)

        print('[%.3fs]: %d %s' % (time.clock() - start_time, num, img_path))
        num += 1


if '__main__':
    main()