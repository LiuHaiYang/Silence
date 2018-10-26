# coding=utf-8
import os
import numpy as np
from PIL import Image, ImageDraw
import cv2
import requests
import json
import time
import asyncio
from threading import Thread


def face_data():
    try:
        face_url = ''
        data = {}
        data['token'] = ''
        face_img = open("./video/face.jpg", 'rb')
        f = {"image": face_img}
        face_result = requests.post(face_url, files=f, data=data)
        # print(face_result.text)
        data_face  = json.loads(face_result.text)
    except:
        data_error = {"error_info":0,"face_num":0,"face_info":[]}
        data_face = json.loads(data_error)
    return data_face

videoCapture = cv2.VideoCapture(0)
fps = videoCapture.get(cv2.CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

count = 0
while 1:
    count +=1
    ret, img = videoCapture.read()
    frame_resize = cv2.resize(img, (size[0], size[1]), interpolation=cv2.INTER_AREA)

    fontface = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 1
    fontcolor = (0, 255, 255)
    face_name_l = []

    faceImage = cv2.imwrite("./video/face.jpg", frame_resize)

    img_tmp = cv2.imread('./video/face.jpg')
    if count % 20 == 0:
        Facedata = face_data()
        # {'error_info': 0, 'face_num': 1, 'face_info': [{'face_id': '0',
        # 'face_location': {'left_top_y': 221.48569,'left_top_x': 534.0691,
        #   'width': 289.12805, 'height': 422.08163},'face_attribute': {'age': 24.104918, 'gender': 1, 'race': 2,
        #  'beauty': 66.07489, 'smile': 15.391903}}],

        if Facedata['error_info'] == 0 and Facedata['face_num'] > 0 :
            print('hvae people')


            #loads image
            for i in range(len(Facedata['face_info'])):
            # for i in range(3):
                left_top_x = int(Facedata['face_info'][i]['face_location']['left_top_x'])
                left_top_y = int(Facedata['face_info'][i]['face_location']['left_top_x'])
                width = int(Facedata['face_info'][i]['face_location']['width'])
                height = int(Facedata['face_info'][i]['face_location']['height'])
                # cropImg = img_tmp[left_top_x:left_top_x + width,left_top_y:left_top_y +height]
                # cropImg = img_tmp[left_top_y:left_top_y + height,left_top_x:left_top_x + width]
                cropImg = img_tmp[left_top_y-int(height*0.6):left_top_y + int(height*0.8),left_top_x:left_top_x + width]
                cv2.imwrite("./face/face_id_"+str(i)+".jpg", cropImg)
            # 鉴别
            try:

                url = ''
                data = {}
                data['token'] = ''
                data['groupId'] = '29'
                data['groupName'] = ''
                data['topN'] = 0
                data['qualityControl'] = 0
                for i in range(len(Facedata['face_info'])):
                    new_img = open("./face/face_id_"+str(i)+".jpg", 'rb')
                    f = {"image": new_img}
                    d = {"muti_det": 1, "url": ""}
                    result = requests.post(url, files=f, data=data)
                    requestdata = result.json()
                    for per_info in requestdata['resultInfo']:
                        if per_info['score'] > 0.6:
                            # print(per_info['userName'])
                            face_name = {"userName":per_info['userName'],"face_id":str(i)}
                            break
                    face_name_l.append(face_name)

            except Exception as e:
                pass

            # for i in face_name_l:
            #     index = int(i['face_id'])
            #     # cv2.putText(faceImage, i['userName'], (
            #     # int(Facedata['face_info'][index]['face_location']['left_top_x']), int(Facedata['face_info'][index]['face_location']['left_top_y'])),
            #     #             fontface, fontscale, fontcolor)
            #     cv2.putText(img_tmp, 'hello', (200, 200), fontface, fontscale, fontcolor)
            # cv2.imshow('video', img_tmp)
            # print('sleep')
            # time.sleep(10)

        else:
            print('no one')
    if face_name_l != []:
        for i in face_name_l:
            index = int(i['face_id'])
            name_x = int(Facedata['face_info'][index]['face_location']['left_top_x'])
            name_y = int(Facedata['face_info'][index]['face_location']['left_top_y'])
            cv2.putText(img_tmp, str(i['userName']), (int(name_x), int(name_y)), fontface, fontscale, fontcolor)
        cv2.imshow('video', img_tmp)
        cv2.waitKey(2*1000)
    cv2.imshow('video', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
videoCapture.release()
cv2.destroyAllWindows()
