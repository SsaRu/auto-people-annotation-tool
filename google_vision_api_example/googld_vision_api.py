# encoding=utf8

import io
from PIL import Image

from google.cloud import vision

'''
this code work on python 2.7
You need 3 installation

1. google-vison-api for python 2.y
2. gcloud-sdk

and you should get auth from gcloud-sdk

Here, is process how to do that

1. how to install google vision api python library?
Google Cloud Vision API Client Library for Python:
https://developers.google.com/api-client-library/python/apis/vision/v1

2. how to install gcloud SDK
https://cloud.google.com/sdk/downloads

2. how to gcloud auth application-default login google vision api
https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login


'''

""" Detects faces in an images"""

vision_client = vision.Client()

image_path = 'lena.jpg'

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

