# auto-people-annotation-tool
auto-people-annotation-tool make deeplearning training dataset about face using google vision api and microsoft azure face api

this code work on python 2.7

### 1. Google Vision API Tool

if you want use google vision api, you should make project in google api console and install 2 kind of library

reference google_vision_api_example in this repository

https://github.com/SsaRu/auto-people-annotation-tool/tree/master/google_vision_api_example

![Google Vision API](https://github.com/SsaRu/auto-people-annotation-tool/blob/master/readme/lenna_test_google.png)

#### 1-1. Make project in Google api

follow this link : https://cloud.google.com/vision/docs/quickstart

#### 1-2. Install gcloud sdk

follow this link : https://cloud.google.com/sdk/docs/

#### 1-3. gcloud auth applicationde-default login

follow this link : https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login

#### 1-4. install google vision api python 

follow this link : https://cloud.google.com/vision/docs/reference/libraries

### 2. Microsoft Azure Face API Tool

if you want using microsoft Azure Face API, just you need httplib library on python2.7

installation httplib on python 2.7 -> pip install httplib2

Reference azure_face_api_example in this repository

https://github.com/SsaRu/auto-people-annotation-tool/tree/master/azure_face_api_example

![Microsoft Azure Face API](https://github.com/SsaRu/auto-people-annotation-tool/blob/master/readme/lenna_test_azure.png)

### 3. Flow Chart

![How to Work](https://github.com/SsaRu/auto-people-annotation-tool/blob/master/readme/flow%20chart.png)

### 4. VOC fascal xml format

it show voc fascal image & annotation xml and result

![image](https://github.com/SsaRu/auto-people-annotation-tool/blob/master/readme/000005.jpg)

![xml](https://github.com/SsaRu/auto-people-annotation-tool/blob/master/readme/annotation.png)

![result](https://github.com/SsaRu/auto-people-annotation-tool/blob/master/readme/000005_result.png)
