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


def split_train_test(data, ratio=0.8):
    assert len(data['annotations']) == len(data['images'])
    num_total = len(data['annotations'])
    num_train = int(num_total * ratio)
    data_train = {'annotations': data['annotations'][:num_train], 'images': data['images'][:num_train]}
    data_test = {'annotations': data['annotations'][num_train:], 'images': data['images'][num_train:]}
    json.dump(data_train, open('coco_train.json', 'w'), indent=4)
    json.dump(data_test, open('coco_test.json', 'w'), indent=4)


def main():
    data = json.load(open('coco.json'))
    # update_filename(data)
    # update_id(data)
    split_train_test(data)
    # json.dump(data, open('coco.json', 'w'), indent=4)
    # print(data['images'][-1])
    # print(data['annotations'][-1])


if __name__ == '__main__':
    main()