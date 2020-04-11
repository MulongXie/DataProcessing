import json
from os.path import join as pjoin
from glob import glob
import cv2

img_id = 0


def clip_images(image_file, sections, output_root, shrink_ratio=4, show=False):
    img = cv2.imread(image_file)
    image = cv2.resize(cv2.imread(image_file), (1440, 2560))
    image_anns = []
    global img_id
    for section in sections:
        clip_path = pjoin(output_root, str(img_id) + '.jpg')
        clip = image[section[1]:section[3], section[0]:section[2]]
        clip = cv2.resize(clip, (int(clip.shape[1]/shrink_ratio), int(clip.shape[0]/shrink_ratio)))
        img_id += 1
        image_anns.append({'file_name':clip_path, 'id':img_id, 'height':section[3]-section[1], 'width':section[2]-section[0]})
        cv2.imwrite(clip_path, clip)

        if show:
            print(clip_path)
            board = image.copy()
            cv2.rectangle(board, (section[0], section[1]), (section[2], section[3]), (255,0,0), 5)
            cv2.imshow('clip', clip)
            cv2.imshow('image', cv2.resize(board, (int(image.shape[1]/shrink_ratio), int(image.shape[0]/shrink_ratio))))
            cv2.waitKey()
    return image_anns


def cvt_coco_format(caption, clip_root):
    annotations = []
    sections = []
    org_image = caption['annotations'][0]['image_path']
    for ann in caption['annotations']:
        annotations.append({'id': ann['id'], 'caption':ann['caption'], 'image_id':ann['image_id'], 'caption_len':ann['caption_size']})
        sections.append(ann['image_section'])
    images = clip_images(org_image, sections, clip_root)
    return annotations, images


def main():
    cap_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-caption'
    clip_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-block-clip'
    caps = glob(pjoin(cap_root, '*.json'))
    caps = sorted(caps, key=lambda x: int(x.split('\\')[-1][:-5]))
    data = {'annotations':[], 'images':[]}
    for i, cap_path in enumerate(caps):
        print(i, cap_path)
        cap = json.load(open(cap_path))
        anns, image = cvt_coco_format(cap, clip_root)
        data['annotations'] += anns
        data['images'] += image

    json.dump(data, open('coco.json', 'w'), indent=4)


if __name__ == '__main__':
    main()