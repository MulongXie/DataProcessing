import json
from glob import glob
from os.path import join as pjoin


def update_img_path(caption):
    name = caption['annotations'][0]['image_path'].split('\\')[-1]
    for ann in caption['annotations']:
        ann['image_path'] = pjoin(img_root, name)


img_root = 'E:\\Mulong\\Datasets\\gui\\rico\\combined'
cap_root = 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-caption'
caps = glob(pjoin(cap_root, '*.json'))
caps = sorted(caps, key=lambda x: int(x.split('\\')[-1][:-5]))
data = {'annotations':[], 'images':[]}
for i, cap_path in enumerate(caps):
    print(i, cap_path)
    cap = json.load(open(cap_path))
    update_img_path(cap)
    json.dump(cap, open(cap_path, 'w'), indent=4)