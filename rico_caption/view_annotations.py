import json
import cv2


def view_annotations(data):
    annotations = data['annotations']
    images = data['images']
    for i, ann in enumerate(annotations):
        img = cv2.imread(images[i]['file_name'])
        print(ann)
        cv2.imshow('img', img)
        cv2.waitKey()


data = json.load(open('coco.json'))
view_annotations(data)