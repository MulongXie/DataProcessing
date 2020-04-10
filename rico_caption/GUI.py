import json
import cv2
import numpy as np
from random import randint as rint
import os


def save_gui_captions(gui_blocks, output_file):
    data = {'annotations':[]}
    for gui_block in gui_blocks:
        ann = {'id' :gui_block.id, 'image_id':gui_block.image_id,
               'image_path': gui_block.image_path,
               'image_section': gui_block.image_section,
               'caption': gui_block.caption,
               'caption_size': gui_block.caption_size}
        data['annotations'].append(ann)
    json.dump(data, open(output_file, 'w'), indent=4)


class GUI_Block:
    def __init__(self, id, subtrees, image_path, image_section):
        self.id = id
        self.subtrees = subtrees
        self.image_path = image_path
        self.image_id = image_path.split('\\')[-1][:-4]
        self.image_section = image_section
        self.image_size = (1440, 2560)
        self.caption = ''
        self.caption_size = 0
        self.max_caption_size = 40

    def generate_caption(self):
        def generate_caption_by_class(tree, caption):
            caption += tree['class'].split('.')[-1]
            self.caption_size += 1
            if 'children' in tree and len(tree['children']) > 0:
                child_caption = ''
                for child in tree['children']:
                    child_caption = generate_caption_by_class(child, child_caption) + ' '
                caption = caption + '{' + child_caption[:-1] + '}'
            return caption

        for subtree in self.subtrees:
            caption = generate_caption_by_class(subtree, self.caption)
            self.caption = caption + ' '
            # print(self.caption)
            # print(self.caption_size)

    def view_gui_tree(self):
        def draw_tree(node, board, line=-1):
            color = (rint(0, 255), rint(0, 255), rint(0, 255))
            cv2.rectangle(board, (node['bounds'][0], node['bounds'][1]), (node['bounds'][2], node['bounds'][3]), color, line)
            cv2.putText(board, node['class'], (int((node['bounds'][0] + node['bounds'][2]) / 2) - 50, int((node['bounds'][1] + node['bounds'][3]) / 2)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
            if 'children' not in node:
                return
            for child in node['children']:
                draw_tree(child, board)

        org = cv2.resize(cv2.imread(self.image_path), self.image_size)
        # label block segmentation
        bounds = self.image_section
        cv2.rectangle(org, (bounds[0], bounds[1]), (bounds[2], bounds[3]), (0, 255, 0), 5)
        # label annotations
        board_tree = np.full((self.image_size[1], self.image_size[0], 3), 255, dtype=np.uint8)
        for subtree in self.subtrees:
            draw_tree(subtree, board_tree)

        cv2.imshow('seg_block', cv2.resize(org, (300, 500)))
        cv2.imshow('seg_tree', cv2.resize(board_tree, (300, 500)))
        cv2.waitKey()
