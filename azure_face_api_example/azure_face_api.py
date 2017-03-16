import httplib, urllib, json

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
}

params = urllib.urlencode({
    # Request parameters
    'subscription-key':'YOUR-FACE-API-KEY',
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender',
})

try:
    open_img = open("../lena.jpg", 'rb')
    body = open_img.read()
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    json_data = json.loads(data)
    print("gender : {}".format(json_data[0]["faceAttributes"]["gender"]))
    print("age : {}".format(json_data[0]["faceAttributes"]["age"]))
    conn.close()
except Exception as e:
    print("[Errno ] : " + e.message)
