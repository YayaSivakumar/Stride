'''
import ast
import os.path
from xml.dom import minidom


#### ONLY ONE OBJECT PER IMAGE IS ASSUMED ####

out_dir = './out'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

file = minidom.parse('annotations.xml')

images = file.getElementsByTagName('image')

for image in images:
    width = int(image.getAttribute('width'))
    height = int(image.getAttribute('height'))
    name = image.getAttribute('name')
    elem = image.getElementsByTagName('points')
    bbox = image.getElementsByTagName('box')
    for b in bbox:
        xtl = int(float(b.attributes['xtl'].value))
        ytl = int(float(b.attributes['ytl'].value))
        xbr = int(float(b.attributes['xbr'].value))
        ybr = int(float(b.attributes['ybr'].value))
    
    w = xbr - xtl
    h = ybr - ytl

    label_file = open(os.path.join(out_dir, name[:-4] + '.txt'), 'w')

    for e in elem:

        label_file.write('0 {} {} {} {} '.format(str((xtl + (w / 2)) / width), str((ytl + (h / 2)) / height),
                                                 str(w / width), str(h / height)))

        points = e.attributes['points']
        points = points.value.split(';')
        points_ = []
        for p in points:
            p = p.split(',')
            p1, p2 = p
            points_.append([int(float(p1)), int(float(p2))])
        for p_, p in enumerate(points_):
            label_file.write('{} {} 2'.format(p[0] / width, p[1] / height))
            if p_ < len(points_) - 1:
                label_file.write(' ')
            else:
                label_file.write('\n')
'''

from ultralytics import YOLO
import cv2

model_path = 'best.pt'
model = YOLO(model_path)
def calculate_points(image_path):
    image_path = image_path
    img = cv2.imread(image_path)

    results = model(image_path)[0]
    list_of_points = []
    for result in results:
        for points in result.keypoints.to().data:
            for keypoint in points:
                x = int(keypoint[0])
                y = int(keypoint[1])
                list_of_points.append((x, y))
                cv2.putText(img, str('.'), (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    return list_of_points

print(calculate_points('f.jpg'))
