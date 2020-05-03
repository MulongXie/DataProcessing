import json
import cv2
from os.path import join as pjoin


def view_annotations(data, image_root):
    annotations = data['annotations']
    images = data['images']
    for i, ann in enumerate(annotations):
        img = cv2.imread(pjoin(image_root, images[i]['file_name']))
        print(ann)
        ratio = 1
        cv2.imshow('img', cv2.resize(img, (int(img.shape[1]/ratio), int(img.shape[0]/ratio))))
        cv2.waitKey()


def main():
    clip_root = 'E:\\Temp\\rico-block-clip'
    data = json.load(open('coco.json'))
    view_annotations(data, clip_root)


if __name__ == '__main__':
    main()