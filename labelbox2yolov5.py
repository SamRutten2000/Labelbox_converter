import json

img_shape = [1920, 1080] #height, widht
label_names = ['Wrinkle_critical', 'Wrinkle_nonCritical'] #Same as 'title' in JSON file
json_name = 'labels.json'


#Open Labelbox JSON
with open(json_name) as json_file:
    data = json.load(json_file)

    for line in data:

        #Create txt file for image
        image_name = line['External ID']
        txt = open('labels/' + image_name.split('.')[0] + '.txt', 'w+')
        print(image_name)

        #For each label
        for label in line['Label']['objects']:

            #Get classification ID
            classification = str(label_names.index(label['title']))

            #Get x_min, x_max, y_min, y_max
            x_coordinates = []
            y_coordinates = []
            for point in label['polygon']:
                x_coordinates.append(point['x'])
                y_coordinates.append(point['y'])
            
            x_min = min(x_coordinates)
            x_max = max(x_coordinates)
            y_min = min(y_coordinates)
            y_max = max(y_coordinates)

            #Calculate normalized center coordinates and width and height from bondingbox
            center_x = str(((x_max+x_min)/2)/img_shape[1])
            center_y = str(((y_max+y_min)/2)/img_shape[0])
            width = str((x_max - x_min)/img_shape[1])
            height = str((y_max-y_min)/img_shape[0])

            #Write label to txt file
            print(classification, center_x, center_y, width, height)
            txt.writelines(classification + ' ' + center_x+ ' ' + center_y+ ' ' + width+ ' ' + height + '\n')

        #Close the txt file
        print('')
        txt.close()
            
