
print('Start program')

file_name = 'labels.json' #filename.json
label_names = ['Wrinkle_critical', 'Wrinkle_nonCritical'] #Same as 'title' in JSON file

import json
import numpy as np
import os
from PIL import Image, ImageDraw


print('Open label JSON')

with open(file_name) as json_file:
    labelbox_data = json.load(json_file)

images = []

print('Create info from JSON')

for data_row in labelbox_data:

    image = {}
    image['filename'] = data_row['External ID']

    regions = []

    #Append polygonoms
    for poly in data_row['Label']['objects']:
        region = {}

        points = [[], []]
        for pnt in poly['polygon']:
            points[0].append(pnt['x'])
            points[1].append(pnt['y'])

        region['shape_attributes'] = {
            'name': 'polygon',
            'all_points_x': points[0],
            'all_points_y': points[1]
            }

        region['region_attributes'] = {
            'name': poly['title'],
            'type': poly['title'],
            "image_quality": {
                "good": True,
                "frontal": True,
                "good_illumination": True
                },
            "none": str(label_names.index(poly['title']))
            }

        regions.append(region)
    image['regions'] = regions

    images.append(image)



print('Create new JSON structure')

via_labels = {}

for img in images:
    via_labels[img['filename']] = img

print('Export JSON')

with open('via_region_data.json', 'w') as outfile:
    json.dump(via_labels, outfile)

print('via labels JSON exported')