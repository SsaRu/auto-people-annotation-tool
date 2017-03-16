# encoding=utf8
import os
import io
import httplib
import urllib
import json
import time
from shutil import copyfile
from google.cloud import vision
from PIL import Image

class color:
    BOLD = '\033[1m'
    END = '\033[0m'
    DEFAULT = '\033[0;37;40m'
    RED = '\033[91m'

# 1. Get Head Boundery Information from Google Vision API and crop & save head image from original image
# 2. Request gender/age information from Microsoft Azure Face API using saved head Image
# 3. Total information convert to VOC style xml format
# 4. Save VOC style xml format

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
}

params = urllib.urlencode({
    # Request parameters
    'subscription-key': 'YOUR-FACE-API-KEY',
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender',
})

# Image directory for analysis example : '/media/martin/SsaRu/Aidentify/deeplearning/Yolo_darknet/darknet/voc/person_img/voc2007/'
img_directory = 'YOUR IMAGE DIRECTORY';
# Folder Name(Image directory) example : "voc2012"
folder_name = "YOUR IMAGE FOLDER NAME"
# Save directory for VOC style xml format
# example : /media/martin/SsaRu/Aidentify/img_set/processing_labeling/label/
save_label_directory ='YOUR LABEL FOLDER NAME'

img_list = []
for img_root, img_dirs, img_files in os.walk('YOUR IMAGE DIRECTORY'):
    img_list = img_files

print("Image List from target folder : ")
print("img_list : {}".format(img_list))
print("Start Detect & Recognize head & Face")
print
print("-------------------------------------------------------------------------------------")
print("-------------------------------------------------------------------------------------")
print

for count in range(0, len(img_list)):

    try:
        print("Open xml file for making VOC style xml file format")
        f = open(str(save_label_directory)+str(img_list[count][:-4])+".xml", 'w')
        if f.closed:
            print("file writing error")
            continue

        # Start xml writing
        f.write("<annotation>\n")

        if count >= len(img_list):
            print("list length : {}".format(len(img_list)))
            print("index finished")
            break

        # target image
        tmp_img_directory = img_directory + img_list[count]
        print("Image file : {}".format(tmp_img_directory))

        #1. Get Head Boundery Information from Google Vision API and crop & save head image from original image
        print("Start Google Vision API")

        f.write("\t<folder>" + str(folder_name) + "</folder>\n")
        f.write("\t<filename>" + str(img_list[count][:-4]) + "</filename>\n")
        f.write("\t<path>" + str(tmp_img_directory) + "</path>\n")
        f.write("\t<source>\n")
        f.write("\t\t<database>Unknown</database>\n")
        f.write("\t</source>\n")
        f.write("\t<size>\n")


        vision_client = vision.Client()
        print("Create Google Vision API SDK object")
        origin_img = Image.open(tmp_img_directory)
        print("Open Origin Image")
        f.write("\t\t<width>" + str(origin_img.size[0]) + "</width>\n")
        f.write("\t\t<height>" + str(origin_img.size[1]) + "</height>\n")
        f.write("\t\t<depth>3</depth>\n")
        f.write("\t</size>\n")
        f.write("\t<segmented>0</segmented>\n")
        print("Write xml header file")

        with io.open(tmp_img_directory, 'rb') as image_file:
            content = image_file.read()

        image = vision_client.image(content=content)
        faces = image.detect_faces()
        print("Read Image file with binary file and Send Image file to Google Cloud Vision API Server")
        faceNum = 0
        empty_cnt = 0
        for face in faces:

            faceNum = faceNum + 1

            if (face.bounds.vertices[0].x_coordinate == None) or (face.bounds.vertices[0].y_coordinate == None) or (face.bounds.vertices[2].x_coordinate == None) or (face.bounds.vertices[2].y_coordinate == None):
                print("bndbox property have a None, skip this image")
                continue

            x1 = face.bounds.vertices[0].x_coordinate
            y1 = face.bounds.vertices[0].y_coordinate
            x2 = face.bounds.vertices[2].x_coordinate
            y2 = face.bounds.vertices[2].y_coordinate
            width = int(face.bounds.vertices[2].x_coordinate) - int(x1)
            height = int(face.bounds.vertices[2].y_coordinate) - int(y1)


            # Delete saved head image before processing
            # example -> "/home/martin/PycharmProjects/head_annotation/tmp.jpg"
            if os.path.exists("YOUR-DIRECTORY"):
                print("delete already exist croped image")
                os.remove("YOUR-DIRECTORY")

            time.sleep(1)

            print("Crop Image from Google Vision API Response")
            box = (x1, y1, x2, y2)
            croped_img = origin_img.crop(box)

            # temporary location for save croped head image
            # example -> "/home/martin/PycharmProjects/head_annotation/tmp.jpg"
            croped_img.save("YOUR-DIRECTORY")
            if not os.path.exists("YOUR-DIRECTORY"):
                print("dont't have croped image, stop")
                continue
            print("Save Croped Image")
            print("End Google Vision API")

            time.sleep(1)

            print("Start MicroSoft Azure Face API")

            ''' 2. Request gender/age information from Microsoft Azure Face API using saved head Image '''

            head_img = open("tmp.jpg")
            body = head_img.read()
            print("MicroSoft Azure Face API Open Head Image & set body variable")
            print("Open Connection")
            conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            print("Send Image to Microsoft Azure Service")
            conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
            response = conn.getresponse()
            print("get response from microsoft Azure")
            data = response.read()
            print("Finished get response data")
            conn.close()
            print("close connection")
            del conn
            print("delete connection")

            if len(data) < 5:
                print(color.BOLD + color.RED + "face is empty or Microsoft Azure response is empty this part skip" + color.END)
                empty_cnt += 1
                continue
            else:
                json_data = json.loads(data)

                gender = json_data[0]["faceAttributes"]["gender"]
                age = json_data[0]["faceAttributes"]["age"]
                print("Read Gender/Age information")
                age_parameter = ""
                gender_parameter = ""

                if 0 <= age and age <=2 :
                    age_parameter = "Baby"
                elif 2 < age and age <= 12:
                    age_parameter = "Young_Child"
                elif 12 < age and age <= 19:
                    age_parameter = "Child"
                elif 19 < age and age <= 29:
                    age_parameter = "Young_Adult"
                elif 29 < age and age <= 39:
                    age_parameter = "Adult"
                elif 39 < age and age <= 49:
                    age_parameter = "Adult"
                elif 49 < age and age <= 59:
                    age_parameter = "Senior"
                elif 59 < age and age <=120:
                    age_parameter = "Senior"
                else:
                    print("age error, skip this loop")
                    continue

                if gender == "male":
                    gender_parameter = "Male_"
                elif gender == "female":
                    gender_parameter = "Female_"
                else:
                    print("gender error, skip this loop")
                    continue

                print("Get and Set Gender & Age Data")

                f.write("\t<object>\n")
                f.write("\t\t<name>" + gender_parameter+age_parameter + "</name>\n")
                f.write("\t\t<pose>Unspecified</pose>\n")
                f.write("\t\t<truncated>0</truncated>\n")
                f.write("\t\t<difficult>0</difficult>\n")
                f.write("\t\t<bndbox>\n")
                f.write("\t\t\t<xmin>"+ str(x1) +"</xmin>\n")
                f.write("\t\t\t<ymin>"+ str(y1) +"</ymin>\n")
                f.write("\t\t\t<xmax>"+ str(x2) +"</xmax>\n")
                f.write("\t\t\t<ymax>"+ str(y2) +"</ymax>\n")
                f.write("\t\t</bndbox>\n")
                f.write("\t</object>\n")

                print("Write Object xml contents")

                # Extract head image
                print("Copy success Face Recognition head img to {}".format('HEAD IMAGE LOCATION FOR SAVE'))
                copyfile("HEAD IMAGE LOCATION", 'HEAD IMAGE LOCATION FOR SAVE')
                print
                print(color.BOLD + color.RED +"Result of Detection : "+ color.END)
                print
                print(color.BOLD + color.RED + "Json Data : {}".format(data) + color.END)
                print(color.BOLD + color.RED +"Head Boundery -> x:{}, y:{}, width: {}, height: {}".format(x1, y1, width, height)+ color.END)
                print(color.BOLD + color.RED +"Person Information -> gender : {}, age : {}".format(gender, age)+ color.END)
                print
        print("Face Detection Loop Finished")
        print("number of Face : {}".format(faceNum))
        print("number of empty Face :{}".format(empty_cnt))

        f.write("</annotation>\n")

        time.sleep(2)

        if f.closed:
            print("file already closed")
        else:
            print("file doesn't close")
            f.close()

        print("xml save directory : {}".format(save_label_directory+img_list[count][:-4]+".xml"))
        print("End MicroSoft Azure Face API")

        if faceNum == 0 or faceNum == empty_cnt:
            print("face can't found, delete xml, delete Image")
            print("delete Image : {}".format(tmp_img_directory))
            if os.path.exists(tmp_img_directory):
                os.remove(tmp_img_directory)
            time.sleep(2)
            raise Exception("face not found in Microsoft Azure")

            time.sleep(1)
            if os.path.exists(save_label_directory+img_list[count][:-4]+".xml"):
                print("xml file delete")
                os.remove(save_label_directory+img_list[count][:-4]+".xml")
        else:
            print("Origin Image Move to save directory : {} to {}".format(tmp_img_directory , 'LOCATION FOR SAVING ORIGINAL IMAGE'))
            copyfile(tmp_img_directory, 'LOCATION FOR SAVING ORIGINAL IMAGE')
            time.sleep(3)
            print("delete Origin Image : {}".format(tmp_img_directory))
            if os.path.exists(tmp_img_directory):
                os.remove(tmp_img_directory)

        print("Sleep during 90 second")
        print("-------------------------------------------------------------------------------------")
        time.sleep(90)

    except IOError as e:
        print("IOError : {}".format(e.message))
        if f.closed:
            print(color.BOLD + color.RED +  "file closed" + color.END)
        else:
            print(color.BOLD + color.RED+ "file doesn't close" + color.END)
            f.close()
        time.sleep(2)

        if os.path.exists(save_label_directory + img_list[count][:-4] + ".xml"):
            os.remove(save_label_directory + img_list[count][:-4] + ".xml")

        time.sleep(90)
        print("-------------------------------------------------------------------------------------")


    except Exception as e:
        print("error, skip this loop, sleep during 30s")
        print(color.BOLD + color.RED +"error message : {}".format(e.message) + color.END)

        if e.message == "Insufficient tokens for quota group and limit 'DefaultGroupUSER-100s' of service 'vision.googleapis.com', using the limit by ID '764086051850@883616541933'. (POST https://vision.googleapis.com/v1/images:annotate)":
            print("too many request, sleep 30s more")
            time.sleep(30)
        if f.closed:
            print("file already closed")
        else:
            print("file doesn't close")
            f.close()
        time.sleep(2)
        print("Delete Image & xml files")
        if os.path.exists(tmp_img_directory):
            os.remove(tmp_img_directory)
        if os.path.exists(save_label_directory + img_list[count][:-4] + ".xml"):
            os.remove(save_label_directory + img_list[count][:-4] + ".xml")
        print("-------------------------------------------------------------------------------------")
        time.sleep(90)
