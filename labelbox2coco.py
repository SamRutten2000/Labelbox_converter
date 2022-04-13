import json
import numpy as np
from PIL import Image, ImageDraw

print('Start program')

img_shape = [1920, 1080] #height, widht
label_names = ['Wrinkle_critical', 'Wrinkle_nonCritical'] #Same as 'title' in JSON file
json_name = 'labels.json'

print('Open label JSON')

with open(json_name) as json_file:
    labelbox_data = json.load(json_file)

images = []
annotations = []

img_id = 0
ann_id = 0

def getbbox(points):
    global img_shape
    polygons = points
    mask = polygons_to_mask(img_shape, polygons)
    return mask2box(mask)

def mask2box(mask):

        index = np.argwhere(mask == 1)
        rows = index[:, 0]
        clos = index[:, 1]

        left_top_r = np.min(rows)  # y
        left_top_c = np.min(clos)  # x

        right_bottom_r = np.max(rows)
        right_bottom_c = np.max(clos)

        return [
            left_top_c,
            left_top_r,
            right_bottom_c - left_top_c,
            right_bottom_r - left_top_r,
        ]

def polygons_to_mask(img_shape, polygons):
        mask = np.zeros(img_shape, dtype=np.uint8)
        mask = Image.fromarray(mask)
        xy = list(map(tuple, polygons))
        ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
        mask = np.array(mask, dtype=bool)
        return mask

print('Create info from JSON')

for data_row in labelbox_data:

    image = {}
    image['id'] = img_id
    image['license'] = 1
    image['file_name'] = data_row['External ID']
    image['height'] = img_shape[0]
    image['widht'] = img_shape[1]
    image['date_caputred'] = data_row['Created At']

    images.append(image)

    #Append polygonoms
    for poly in data_row['Label']['objects']:
        annotation = {}

        points = []
        seg = []
        for pnt in poly['polygon']:
            points.append([pnt['x'], pnt['y']])
            seg.append(pnt['x'])
            seg.append(pnt['y'])

        contour = np.array(points)
        x = contour[:, 0]
        y = contour[:, 1]
        
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

        annotation["segmentation"] = [seg]
        annotation["iscrowd"] = 0
        annotation["area"] = area
        annotation["image_id"] = img_id

        annotation["bbox"] = list(map(float, getbbox(points)))

        cat_id = label_names.index(poly['title'])

        annotation["category_id"] = cat_id 
        annotation["id"] = ann_id

        annotations.append(annotation)
        ann_id +=1

    img_id+=1

print('Create new JSON structure')

coco_struc= {
    'info': {
        'year': '2022', 
        'version': '1',
        "description": "Translated from labelbox",
        "contributor": "User",
        }, 
    'licenses': [{
        "id": 1,
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "name": "Public Domain"
        }],
    "categories": [
        {
            "id": 0,
            "name": "wrinkle_critical",
            "supercategory": "none"
        },
        {
            "id": 1,
            "name": "wrinkle_nonCritical",
            "supercategory": "none"
        }],
    'images': images,
    'annotations': annotations
    }

print('Export JSON')

with open('labels_coco.json', 'w') as outfile:
    json.dump(coco_struc, outfile)

print('coco JSON exported')