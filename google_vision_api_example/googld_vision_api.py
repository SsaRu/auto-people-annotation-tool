# encoding=utf8

import io
from google.cloud import vision

""" Detects faces in an images"""

vision_client = vision.Client()

image_path = '../lena.jpg'

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision_client.image(content=content)

faces = image.detect_faces()

print('Faces :')
faceNum = 0
for face in faces:
    faceNum += 1
    print('bounds x1: {}'.format(face.bounds.vertices[0].x_coordinate))
    print('bounds y1: {}'.format(face.bounds.vertices[0].y_coordinate))
    print('bounds x4: {}'.format(face.bounds.vertices[2].x_coordinate))
    print('bounds y4: {}'.format(face.bounds.vertices[2].y_coordinate))
    print
print("number of Face : {}".format(faceNum))

