#coding=utf-8
#基于python的人脸识别（检测人脸、眼睛、嘴巴、鼻子......）
import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml' )
eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml' )
mouth_cascade = cv2.CascadeClassifier('./data/haarcascade_mcs_mouth.xml' )
nose_cascade = cv2.CascadeClassifier('./data/haarcascade_mcs_nose.xml' )
leftear_cascade = cv2.CascadeClassifier('./data/haarcascade_mcs_leftear.xml' )
rightear_cascade = cv2.CascadeClassifier('./data/haarcascade_mcs_rightear.xml' )

# 打开摄像头获取视频
cap = cv2.VideoCapture( 0 )
# 编译并输出保存视频
fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
size = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
fourcc = cv2.cv.CV_FOURCC('I','4','2','0')
out = cv2.VideoWriter("./voide/output2.avi",fourcc, 5, size)
print cap.isOpened()
# 无限循环
while ( True ) :
# 获取视频及返回状态
    ret, img = cap.read()
    # 将获取的视频转化为灰色
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    # 检测视频中的人脸，并用 vector 保存人脸的坐标、大小（用矩形表示）
    faces = face_cascade.detectMultiScale(gray, 1.3, 5 )
    # 脸部检测
    for (x,y,w,h) in faces:
        cv2.rectangle( img, ( x,y ) , ( x+w,y+h ) , ( 255,0,0 ) ,2 )
        roi_gray = gray [ y:y+h, x:x+w ]
        roi_color = img [ y:y+h, x:x+w ]
    # 检测视频中脸部的眼睛，并用 vector 保存眼睛的坐标、大小（用矩形表示）
    eyes = eye_cascade.detectMultiScale(roi_gray)
    # 眼睛检测
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color, (ex,ey) , (ex+ew,ey+eh),(0,255,0),2)
    #嘴巴
    mouth = mouth_cascade.detectMultiScale(roi_gray, 1.5,5)
    for (mx, my, mw, mh) in mouth:
        cv2.rectangle(roi_color, (mx, my), (mx+mw, my+mh), (0, 0, 255), 1)
    #鼻子
    nose = nose_cascade.detectMultiScale(roi_gray, 1.2, 5)
    for (nx, ny, nw, nh) in nose:
        cv2.rectangle(roi_color, (nx, ny), (nx+nw, ny+nh), (255, 0, 255), 1)
 
    #耳朵
    leftear = leftear_cascade.detectMultiScale(roi_gray,1.01, 2)
    for (lx, ly, lw, lh) in leftear:
        cv2.rectangle(roi_color, (lx, ly), (lx+lw, ly+lh), (0, 0, 0), 2)
          
    rightear = rightear_cascade.detectMultiScale(roi_gray, 1.01, 2)
    for (rx, ry, rw, rh) in rightear:
        cv2.rectangle(roi_color, (rx, ry), (rx+rw, ry+rh), (0, 0, 0), 2)
          
    # 显示原图像
    out.write(img)
    cv2.imshow ('voide',img)
        # 按 q 键退出 while 循环
    if cv2.waitKey(30) & 0xFF == ord('q') :
    	break
# 关闭视频输出
out.release()        
# 释放摄像头
cap.release()
# 关闭所有窗口
cv2.destroyAllWindows()

