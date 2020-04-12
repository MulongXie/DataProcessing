import json


def update_id(data):
    annotations = data['annotations']
    images = data['images']
    for i, ann in enumerate(annotations):
        ann['id'] = i
        ann['image_id'] = i
        images[i]['id'] = i
        print(i)


def update_filename(data):
    images = data['images']
    for i, image in enumerate(images):
        print(i)
        image['file_name'] = image['file_name'].split('\\')[-1]


data = json.load(open('coco.json'))
update_filename(data)
# update_id(data)
json.dump(data, open('coco.json', 'w'), indent=4)
print(data['images'][-1])
print(data['annotations'][-1])