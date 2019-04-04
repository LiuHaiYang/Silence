# coding=utf-8
import os
import numpy as np
from PIL import Image, ImageDraw
import cv2
import requests
import io
import json


videoCapture = cv2.VideoCapture(0)
fps = videoCapture.get(cv2.CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# video = cv2.VideoWriter("./video/face.avi", fourcc, 5, size)

while 1:
    ret, img = videoCapture.read()
    img_encode = cv2.imencode('./face1.jpg',img)

    #转换
    #可以看出第二个元素是矩阵
    # print(img_encode)
    str_encode = img_encode[1].tostring()
    # print(str_encode)
    new_img = io.BytesIO(str_encode)
    # print(new_img)


    url_face = ""
    # new_img = open("./video/1.jpg", 'rb')
    f = {"image": new_img}
    d = {"muti_det": 2, "url": ""}
    r = requests.post(url_face, files=f, data=d)
    key_data = json.loads(r.content)
    cv2.imshow('video', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# video.release()
videoCapture.release()
cv2.destroyAllWindows()
