# coding:utf-8
import cv2

## opening videocapture
cap = cv2.VideoCapture(0)

## some videowriter props
sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

fps = 20
#fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#fourcc = cv2.VideoWriter_fourcc('m', 'p', 'e', 'g')
fourcc = cv2.VideoWriter_fourcc(*'mpeg')

## open and set props
vout = cv2.VideoWriter()
vout.open("./voide/output.avi",fourcc,fps,sz,True)

while 1:
    _, frame = cap.read()
    #cv2.putText(frame, str(cnt), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1, cv2.LINE_AA)
    vout.write(frame)
    cv2.imshow('voide',frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

vout.release()
cap.release()
