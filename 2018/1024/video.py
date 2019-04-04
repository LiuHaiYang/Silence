# coding=utf-8
import os
import numpy as np
from PIL import Image, ImageDraw
import cv2
import requests
import json


videoCapture = cv2.VideoCapture(0)
fps = videoCapture.get(cv2.CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# video = cv2.VideoWriter("./video/face.avi", fourcc, 5, size)

while 1:
    ret, img = videoCapture.read()
    cv2.imshow('video', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# video.release()
videoCapture.release()
cv2.destroyAllWindows()