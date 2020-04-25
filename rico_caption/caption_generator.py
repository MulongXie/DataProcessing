import cv2
import json
from os.path import join as pjoin
import os
import time

from GUI import GUI_Block, save_gui_captions


def init_GUI_blocks(gui_block_id, img_path, segments, output_file, show=False):
    guis = []
    for segment in segments['segments']:
        bounds = segment['block']
        subtrees = segment['subtree']

        gui = GUI_Block(gui_block_id, subtrees, img_path, bounds)
        gui.generate_caption()
        if show:
            print(gui.caption_size, gui.caption)
            gui.view_gui_tree()
        if gui.caption_size > gui.max_caption_size:
            continue
        guis.append(gui)
        gui_block_id += 1

    if len(guis) > 0:
        save_gui_captions(guis, output_file)
    return gui_block_id


def main():
    start = 0  # start point
    end = 100000
    gui_block_id = 0
    bad = 0
    img_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\all\\'
    segment_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-subtree\\'
    output_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-caption\\'

    for index in range(start, end):
        img_path = pjoin(img_root, str(index) + '.jpg')
        segment_path = pjoin(segment_root, str(index) + '.json')
        output_path = pjoin(output_root, str(index) + '.json')
        time_s = time.clock()
        if not os.path.exists(segment_path):
            continue
        segments = json.load(open(segment_path))
        gui_block_id = init_GUI_blocks(gui_block_id, img_path, segments, output_path, show=False)
        print('[%.3fs]' %(time.clock() - time_s), segment_path)


if __name__ == '__main__':
    main()