# encoding:utf-8
from PIL import Image, ImageDraw
import requests
import os
from flask import Flask, request,render_template,jsonify
from werkzeug.utils import secure_filename
import uuid
import numpy
import time
import base64
import math
import json
from requests_toolbelt  import MultipartEncoder
UPLOAD_FOLDER = './imageuploads/'
ALLOWED_EXTENSIONS = set(['jpg', 'png','jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/humanbody/api/v1.0', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #save image and  need remove old  image file
            filename = secure_filename(file.filename)
            file_name = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
            sourceFileName = './imageuploads/' + str(file_name)
            #image size change
            file_name_c = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            fsize = round(os.path.getsize(sourceFileName) / float(1024 * 1024),2)
            print('old----->',fsize) #MB
            im = Image.open(sourceFileName)
            print('class', im.format, '，size', im.size, '，colour', im.mode)
            image_change_Filename = './image_change/' + str(file_name_c)
            if fsize > 1.95 :
                if max(im.size[0], im.size[1]) > 4000:
                    im.thumbnail((im.size[0]-1000, im.size[1]-1000))
                    im.save( image_change_Filename, quality=90)
            else:
                im.save(image_change_Filename, quality=90)
            os.remove(sourceFileName)# delete the old files and use zip file

            fsize = round(os.path.getsize(image_change_Filename) / float(1024 * 1024), 2)
            print('change--->',fsize)  # MB
            # # face natural data
            try :
                url_face = ''
                img_face = open(image_change_Filename, 'rb')
                f = {"image": img_face}
                d_face = {'token': '', "url": "", 'face_detect_num': '100'}
                result_face = requests.post(url_face, files=f, data=d_face)
                print('face---->',result_face.json())
                result_face_d = result_face.json()

                if int(result_face.json()['error_info']) !=0:
                    result_face_d = {}
                    # return jsonify({'code':1,'message':'face natural error'})
            except:
                result_face_d = {}
                # return jsonify({'code': 1, 'message': 'face natural error'})
            try:
                # humanbody key data
                url_human=""
                d_human={"muti_det":2,"url":''}
                img_human = open(image_change_Filename, 'rb')
                f_human = {"image": img_human}
                result_body = requests.post(url_human, files=f_human, data=d_human)
                print('Human------>',result_body.json())
                if result_body.json()['error_info'] !=0:
                    result_body_d = {}
                    return jsonify({'errorinfo': 2, 'message': 'face keys error','humanbodydata':result_body_d,'facedata' :json.loads(result_face_d)})
            except:
                result_body_d = {}
                return jsonify({'errorinfo': 2, 'message': 'face keys error','humanbodydata':result_body_d,'facedata' :json.loads(result_face_d)})

            data_p = []
            try:
                for i in result_body.json()['det_info']:
                    dir_d = {}
                    for j in range(3,len(i['node_info']),4):
                        dir_d[i['node_info'][j]]=[i['node_info'][j-3],i['node_info'][j-2]]
                    data_p.append(dir_d)
            except:
                return ""
            # img_head = base64.b64encode(open('./static/0912/head.png','rb').read())
            # img_body = base64.b64encode(open('./static/0912/body.png','rb').read())
            # img_leg_l = base64.b64encode(open('./static/0912/leg_l.png','rb').read())
            # img_leg_r = base64.b64encode(open('./static/0912/leg_r.png','rb').read())
            # img_foot_l = base64.b64encode(open('./static/0912/foot_l.png','rb').read())
            # img_foot_r = base64.b64encode(open('./static/0912/foot_r.png','rb').read())
            # img_arm_r = base64.b64encode(open('./static/0912/arm_r.png','rb').read())
            # img_arm_l = base64.b64encode(open('./static/0912/arm_l.png','rb').read())
            # img_hand_r = base64.b64encode(open('./static/0912/hand_r.png','rb').read())
            # img_hand_l = base64.b64encode(open('./static/0912/hand_l.png','rb').read())
            img_head ='head.png'
            img_body ='body.png'
            img_leg_l='leg_l.png'
            img_leg_r='leg_r.png'
            img_foot_l='foot_l.png'
            img_foot_r='foot_r.png'
            img_arm_r='arm_r.png'
            img_arm_l='arm_l.png'
            img_hand_r='hand_r.png'
            img_hand_l='hand_l.png'

            res=[]
            for d_p in data_p:
                dic_data = {}

                #  body centos
                body_centos_x = int((d_p['r_shoulder'][0]+d_p['l_hip'][0]+d_p['r_hip'][0])/3)
                body_centos_y = int((d_p['r_shoulder'][1]+d_p['l_hip'][1]+d_p['r_hip'][1])/3)-60
                dic_data['body_centos']={'x':body_centos_x,'y':body_centos_y}

                # all body OR  half bpdy
                # if hip >
                dic_data['body_label'] = '0'

                #dic_data = {'head':{'h':50,'w':40,'x':200,'y':100,'angle':15,'image_data':img_head},}
                # head's hight w
                head_w, head_h = int(d_p['neck'][1]) - int(d_p['head'][1]), int(d_p['neck'][1]) - int(d_p['head'][1])
                # need add  condition : + -  > 90   three class expct
                if d_p['neck'][0] == d_p['head'][0] and d_p['neck'][1] == d_p['head'][1]:
                    angle_head = 0
                #head left
                elif d_p['neck'][0] > d_p['head'][0] and d_p['neck'][1] > d_p['head'][1]:
                    angle_head = 0 - (triangle_angle(d_p['head'][0],d_p['head'][1],d_p['neck'][0],d_p['neck'][1],d_p['head'][0],d_p['neck'][1]))
                #head right
                elif d_p['neck'][0] < d_p['head'][0] and d_p['neck'][1] > d_p['head'][1]:
                    angle_head = triangle_angle(d_p['head'][0],d_p['head'][1],d_p['neck'][0],d_p['neck'][1],d_p['head'][0],d_p['neck'][1])
                #other
                else:
                    angle_head = 0

                dic_data['head']={'w':head_w,'h':head_h,'x':d_p['head'][0],'y':d_p['head'][1],'angle':angle_head,'image_data':img_head}

                # face natual data  to body
                if not result_face_d:
                    dic_data['face_num'] = '99'
                else:
                    for face_n in result_face_d['face_info']:
                        print(face_n)
                        x1,x2 = int(face_n['face_location']['left_top_x']),int(face_n['face_location']['left_top_x'])+int(face_n['face_location']['width'])
                        y1,y2 = int(face_n['face_location']['left_top_y']),int(face_n['face_location']['left_top_y'])+int(face_n['face_location']['height'])
                        if d_p['head'][0] > x1 and  d_p['head'][0] < x2 and d_p['head'][1] >y1 and  d_p['head'][1] <y2:
                            dic_data['face_num']=str(face_n['face_id'])

                # body's h w
                body_w, body_h = d_p['l_shoulder'][0] - d_p['r_shoulder'][0] + 50, d_p['l_hip'][1] - d_p['neck'][1]
                # need add  condition : + -  > 90   three class expct
                if d_p['neck'][0] == (d_p['l_hip'][0]+d_p['r_hip'][0])/2 and d_p['l_hip'][1] > d_p['neck'][1] and d_p['r_hip'][1] > d_p['neck'][1]:
                    angle_body = 0
                # head left
                elif d_p['l_hip'][1] > d_p['r_hip'][1] :
                    angle_body = 0-(triangle_angle(d_p['l_hip'][0],d_p['l_hip'][1],d_p['r_hip'][0],d_p['r_hip'][1],d_p['r_hip'][0],d_p['l_hip'][1]))
                # head right
                elif d_p['l_hip'][1] < d_p['r_hip'][1]:
                    angle_body = triangle_angle(d_p['r_hip'][0],d_p['r_hip'][1],d_p['l_hip'][0],d_p['l_hip'][1],d_p['l_hip'][0],d_p['r_hip'][1])
                # other
                else:
                    angle_body = 0
                dic_data['body'] = {'w': body_w, 'h': body_h, 'x':d_p['r_shoulder'][0], 'y': d_p['r_shoulder'][1],'angle': angle_body,'image_data':img_body}  #d_p['r_shoulder'][0] - 55, d_p['r_shoulder'][1] - 30

                # arm's h w
                arm_x = (d_p['l_elbow'][1] - d_p['l_shoulder'][1]) ** 2
                arm_y = (d_p['l_shoulder'][0] - d_p['l_elbow'][0]) ** 2
                l_arm_w, l_arm_h = 30, int(numpy.sqrt( arm_x+arm_y ))
                # eight class
                if d_p['l_elbow'][0] == d_p['l_shoulder'][0] and d_p['l_elbow'][1] > d_p['l_shoulder'][1]:
                    angle_arm_l = 0
                elif d_p['l_elbow'][0] == d_p['l_shoulder'][0] and d_p['l_elbow'][1] > d_p['l_shoulder'][1]:
                    angle_arm_l = 180

                elif d_p['l_elbow'][0] < d_p['l_shoulder'][0] and d_p['l_elbow'][1] == d_p['l_shoulder'][1]:
                    angle_arm_l = 90
                elif d_p['l_elbow'][0] > d_p['l_shoulder'][0] and d_p['l_elbow'][1] == d_p['l_shoulder'][1]:
                    angle_arm_l = -90

                elif d_p['l_elbow'][0] < d_p['l_shoulder'][0] and d_p['l_elbow'][1] > d_p['l_shoulder'][1]:
                    angle_arm_l = triangle_angle(d_p['l_shoulder'][0],d_p['l_shoulder'][1],d_p['l_elbow'][0],d_p['l_elbow'][1],d_p['l_shoulder'][0],d_p['l_elbow'][1])

                elif d_p['l_elbow'][0] < d_p['l_shoulder'][0] and d_p['l_elbow'][1] < d_p['l_shoulder'][1]:
                    angle_arm_l = 90 + triangle_angle(d_p['l_shoulder'][0],d_p['l_shoulder'][1],d_p['l_elbow'][0],d_p['l_elbow'][1],d_p['l_elbow'][0],d_p['l_shoulder'][1])

                elif d_p['l_elbow'][0] > d_p['l_shoulder'][0] and d_p['l_elbow'][1] < d_p['l_shoulder'][1]:
                    angle_arm_l = 180 + triangle_angle(d_p['l_elbow'][0],d_p['l_elbow'][1],d_p['l_shoulder'][0],d_p['l_shoulder'][1],d_p['l_elbow'][0],d_p['l_shoulder'][1])

                elif d_p['l_elbow'][0] > d_p['l_shoulder'][0] and d_p['l_elbow'][1] > d_p['l_shoulder'][1]:
                    angle_arm_l = 0-triangle_angle(d_p['l_shoulder'][0], d_p['l_shoulder'][1], d_p['l_elbow'][0], d_p['l_elbow'][1], d_p['l_shoulder'][0], d_p['l_elbow'][1])
                else:
                    angle_arm_l = 0
                dic_data['arm_l'] = {'w': l_arm_w, 'h': l_arm_h,  'x': d_p['l_shoulder'][0],'y': d_p['l_shoulder'][1],'angle': angle_arm_l,'image_data':img_arm_l}  #d_p['r_shoulder'][0]-10, d_p['r_shoulder'][1]

                r_arm_w, r_arm_h = 30, int(numpy.sqrt((d_p['r_elbow'][1]-d_p['r_shoulder'][1])**2 + (d_p['r_shoulder'][0]-d_p['r_elbow'][0])**2))
                # eight class
                if d_p['r_elbow'][0] == d_p['r_shoulder'][0] and d_p['r_elbow'][1] > d_p['r_shoulder'][1]:
                    angle_arm_r = 0
                elif d_p['r_elbow'][0] == d_p['r_shoulder'][0] and d_p['r_elbow'][1] > d_p['r_shoulder'][1]:
                    angle_arm_r = 180

                elif d_p['r_elbow'][0] < d_p['r_shoulder'][0] and d_p['r_elbow'][1] == d_p['r_shoulder'][1]:
                    angle_arm_r = 90
                elif d_p['r_elbow'][0] > d_p['r_shoulder'][0] and d_p['r_elbow'][1] == d_p['r_shoulder'][1]:
                    angle_arm_r = -90

                elif d_p['r_elbow'][0] < d_p['r_shoulder'][0] and d_p['r_elbow'][1] > d_p['r_shoulder'][1]:
                    angle_arm_r = triangle_angle(d_p['r_shoulder'][0],d_p['r_shoulder'][1],d_p['r_elbow'][0],d_p['r_elbow'][1],d_p['r_shoulder'][0],d_p['r_elbow'][1])

                elif d_p['r_elbow'][0] < d_p['r_shoulder'][0] and d_p['r_elbow'][1] < d_p['r_shoulder'][1]:
                    angle_arm_r = 90 + triangle_angle(d_p['r_shoulder'][0],d_p['r_shoulder'][1],d_p['r_elbow'][0],d_p['r_elbow'][1],d_p['r_elbow'][0],d_p['r_shoulder'][1])

                elif d_p['r_elbow'][0] > d_p['r_shoulder'][0] and d_p['r_elbow'][1] < d_p['r_shoulder'][1]:
                    angle_arm_r = 180 + triangle_angle(d_p['l_elbow'][0],d_p['l_elbow'][1],d_p['r_shoulder'][0],d_p['r_shoulder'][1],d_p['l_elbow'][0],d_p['r_shoulder'][1])

                elif d_p['r_elbow'][0] > d_p['r_shoulder'][0] and d_p['r_elbow'][1] > d_p['r_shoulder'][1]:
                    angle_arm_r = 0-triangle_angle(d_p['r_shoulder'][0], d_p['r_shoulder'][1], d_p['l_elbow'][0], d_p['l_elbow'][1], d_p['r_shoulder'][0], d_p['l_elbow'][1])
                else:
                    angle_arm_r = 0
                dic_data['arm_r'] = {'w': r_arm_w, 'h': r_arm_h,'x':d_p['r_shoulder'][0]-10, 'y': d_p['r_shoulder'][1],'angle': angle_arm_r,'image_data':img_arm_r}  # d_p['l_shoulder'][0]+10, d_p['l_shoulder'][1]

                ## hand's w h

                l_hand_w, l_hand_h = 30, int(numpy.sqrt(( d_p['l_wrist'][0]-d_p['l_elbow'][0])**2+(d_p['l_wrist'][1]-d_p['l_elbow'][1])**2))+40
                # angle_hand_l = 15
                # eight class
                if d_p['l_wrist'][0] == d_p['l_elbow'][0] and d_p['l_wrist'][1] > d_p['l_elbow'][1]:
                    angle_hand_l = 0
                elif d_p['l_wrist'][0] == d_p['l_elbow'][0] and d_p['l_wrist'][1] > d_p['l_elbow'][1]:
                    angle_hand_l = 180

                elif d_p['l_wrist'][0] < d_p['l_elbow'][0] and d_p['l_wrist'][1] == d_p['l_elbow'][1]:
                    angle_hand_l = 90
                elif d_p['l_wrist'][0] > d_p['l_elbow'][0] and d_p['l_wrist'][1] == d_p['l_elbow'][1]:
                    angle_hand_l = -90

                elif d_p['l_wrist'][0] < d_p['l_elbow'][0] and d_p['l_wrist'][1] > d_p['l_elbow'][1]:
                    angle_hand_l = triangle_angle(d_p['l_elbow'][0],d_p['l_elbow'][1],d_p['l_wrist'][0],d_p['l_wrist'][1],d_p['l_elbow'][0],d_p['l_wrist'][1])

                elif d_p['l_wrist'][0] < d_p['l_elbow'][0] and d_p['l_wrist'][1] < d_p['l_elbow'][1]:
                    angle_hand_l = 90 + triangle_angle(d_p['l_elbow'][0],d_p['l_elbow'][1],d_p['l_wrist'][0],d_p['l_wrist'][1],d_p['l_wrist'][0],d_p['l_elbow'][1])

                elif d_p['l_wrist'][0] > d_p['l_elbow'][0] and d_p['l_wrist'][1] < d_p['l_elbow'][1]:
                    angle_hand_l = 180 + triangle_angle(d_p['l_wrist'][0],d_p['l_wrist'][1],d_p['l_elbow'][0],d_p['l_elbow'][1],d_p['l_wrist'][0],d_p['l_elbow'][1])

                elif d_p['l_wrist'][0] > d_p['l_elbow'][0] and d_p['l_wrist'][1] > d_p['l_elbow'][1]:
                    angle_hand_l = 0-triangle_angle(d_p['l_elbow'][0], d_p['l_elbow'][1], d_p['l_wrist'][0], d_p['l_wrist'][1], d_p['l_elbow'][0], d_p['l_wrist'][1])
                else:
                    angle_hand_l = 0

                dic_data['hand_l'] = {'w': l_hand_w, 'h': l_hand_h, 'x': d_p['l_elbow'][0], 'y': d_p['l_elbow'][1], 'angle': angle_hand_l,'image_data':img_hand_l}  # d_p['l_elbow'][0], d_p['l_elbow'][1]

                r_hand_w, r_hand_h = 30, int(numpy.sqrt(( d_p['r_wrist'][0]-d_p['r_elbow'][0])**2+(d_p['r_wrist'][1]-d_p['r_elbow'][1])**2))
                # angle_hand_r = 15
                # eight class
                if d_p['r_wrist'][0] == d_p['r_elbow'][0] and d_p['r_wrist'][1] > d_p['r_elbow'][1]:
                    angle_hand_r = 0
                elif d_p['r_wrist'][0] == d_p['r_elbow'][0] and d_p['r_wrist'][1] > d_p['r_elbow'][1]:
                    angle_hand_r = 180

                elif d_p['r_wrist'][0] < d_p['r_elbow'][0] and d_p['r_wrist'][1] == d_p['r_elbow'][1]:
                    angle_hand_r = 90
                elif d_p['r_wrist'][0] > d_p['r_elbow'][0] and d_p['r_wrist'][1] == d_p['r_elbow'][1]:
                    angle_hand_r = -90

                elif d_p['r_wrist'][0] < d_p['r_elbow'][0] and d_p['r_wrist'][1] > d_p['r_elbow'][1]:
                    angle_hand_r = triangle_angle(d_p['r_elbow'][0],d_p['r_elbow'][1],d_p['r_wrist'][0],d_p['r_wrist'][1],d_p['r_elbow'][0],d_p['r_wrist'][1])

                elif d_p['r_wrist'][0] < d_p['r_elbow'][0] and d_p['r_wrist'][1] < d_p['r_elbow'][1]:
                    angle_hand_r = 90 + triangle_angle(d_p['r_elbow'][0],d_p['r_elbow'][1],d_p['r_wrist'][0],d_p['r_wrist'][1],d_p['r_wrist'][0],d_p['r_elbow'][1])

                elif d_p['r_wrist'][0] > d_p['r_elbow'][0] and d_p['r_wrist'][1] < d_p['r_elbow'][1]:
                    angle_hand_r = 180 + triangle_angle(d_p['r_wrist'][0],d_p['r_wrist'][1],d_p['r_elbow'][0],d_p['r_elbow'][1],d_p['r_wrist'][0],d_p['r_elbow'][1])

                elif d_p['r_wrist'][0] > d_p['r_elbow'][0] and d_p['r_wrist'][1] > d_p['r_elbow'][1]:
                    angle_hand_r = 0-triangle_angle(d_p['r_elbow'][0], d_p['r_elbow'][1], d_p['r_wrist'][0], d_p['r_wrist'][1], d_p['r_elbow'][0], d_p['l_wrist'][1])
                else:
                    angle_hand_r = 0
                dic_data['hand_r'] = {'w': r_hand_w, 'h': r_hand_h, 'x': d_p['r_elbow'][0],'y': d_p['r_elbow'][1], 'angle': angle_hand_r,'image_data':img_hand_r}  #d_p['l_elbow'][0], d_p['l_elbow'][1]

                # leg's h w
                if d_p['l_hip'][1] > d_p['l_knee'][1]:
                    pass
                else:
                    l_leg_w, l_leg_h = 30, int(numpy.sqrt((d_p['l_knee'][0]-d_p['l_hip'][0])**2+(d_p['l_knee'][1]-d_p['l_hip'][1])**2))
                    # three class
                    #angle_leg_l = 5
                    if d_p['l_hip'][0] == d_p['l_knee'][0] and d_p['l_hip'][0] < d_p['l_knee'][0]:
                        angle_leg_l = 0

                    elif d_p['l_hip'][0] > d_p['l_knee'][0] and d_p['l_hip'][1] < d_p['l_knee'][1]:
                        angle_leg_l = triangle_angle(d_p['l_hip'][0],d_p['l_hip'][1],d_p['l_knee'][0],d_p['l_knee'][1],d_p['l_hip'][0],d_p['l_knee'][1])
                    elif d_p['l_hip'][0] < d_p['l_knee'][0] and d_p['l_hip'][1] < d_p['l_knee'][1]:
                        angle_leg_l = 0 - triangle_angle(d_p['l_hip'][0],d_p['l_hip'][1],d_p['l_knee'][0],d_p['l_knee'][1],d_p['l_hip'][0],d_p['l_knee'][1])
                    else:
                        angle_leg_l = 0

                    dic_data['leg_l'] = {'w': l_leg_w, 'h': l_leg_h, 'x': d_p['l_hip'][0], 'y': d_p['l_hip'][1],'angle': angle_leg_l,'image_data':img_leg_l}  # d_p['l_knee'][0], d_p['l_knee'][1]

                if d_p['r_hip'][1] > d_p['r_knee'][1]:
                    pass
                else:
                    r_leg_w, r_leg_h = 30, int(numpy.sqrt((d_p['r_knee'][0] - d_p['r_hip'][0]) ** 2 + (d_p['r_knee'][1] - d_p['r_hip'][1]) ** 2))
                    # angle_leg_r = 5
                    if d_p['r_hip'][0] == d_p['r_knee'][0] and d_p['r_hip'][0] < d_p['r_knee'][0]:
                        angle_leg_r = 0

                    elif d_p['r_hip'][0] > d_p['r_knee'][0] and d_p['r_hip'][1] < d_p['r_knee'][1]:
                        angle_leg_r = triangle_angle(d_p['r_hip'][0],d_p['r_hip'][1],d_p['r_knee'][0],d_p['r_knee'][1],d_p['r_hip'][0],d_p['r_knee'][1])
                    elif d_p['r_hip'][0] < d_p['l_knee'][0] and d_p['r_hip'][1] < d_p['l_knee'][1]:
                        angle_leg_r = 0 - triangle_angle(d_p['r_hip'][0],d_p['r_hip'][1],d_p['r_knee'][0],d_p['r_knee'][1],d_p['r_hip'][0],d_p['r_knee'][1])
                    else:
                        angle_leg_r = 0

                    dic_data['leg_r'] = {'w': r_leg_w, 'h': r_leg_h, 'x': d_p['r_hip'][0], 'y': d_p['r_hip'][1], 'angle': angle_leg_r,'image_data':img_leg_r}  # d_p['l_knee'][0], d_p['l_knee'][1]

                # foot's  h w
                if d_p['l_knee'][1] > d_p['l_ankle'][1]:
                    pass
                else:
                    l_foot_w, l_foot_h = 30,  int(numpy.sqrt((d_p['l_ankle'][0]-d_p['l_knee'][0])**2+(d_p['l_ankle'][1]-d_p['l_knee'][1])**2)+50)
                    # angle_foot_l = 0
                    if d_p['l_knee'][0] == d_p['l_ankle'][0] and d_p['l_knee'][0] < d_p['l_ankle'][0]:
                        angle_foot_l = 0

                    elif d_p['l_knee'][0] > d_p['l_ankle'][0] and d_p['l_knee'][1] < d_p['l_ankle'][1]:
                        angle_foot_l = triangle_angle(d_p['l_knee'][0],d_p['l_knee'][1],d_p['l_ankle'][0],d_p['l_ankle'][1],d_p['l_knee'][0],d_p['l_ankle'][1])
                    elif d_p['l_knee'][0] < d_p['l_ankle'][0] and d_p['l_knee'][1] < d_p['l_ankle'][1]:
                        angle_foot_l = 0 - triangle_angle(d_p['l_knee'][0],d_p['l_knee'][1],d_p['l_ankle'][0],d_p['l_ankle'][1],d_p['l_knee'][0],d_p['l_ankle'][1])
                    else:
                        angle_foot_l = 0
                    dic_data['foot_l'] = {'w': l_foot_w, 'h': l_foot_h, 'x': d_p['l_knee'][0], 'y': d_p['l_knee'][1],'angle': angle_foot_l,'image_data':img_foot_l}  # d_p['r_knee'][0], d_p['r_knee'][1]

                if d_p['r_knee'][1] > d_p['r_ankle'][1]:
                    pass
                else:
                    r_foot_w, r_foot_h = 30,  int(numpy.sqrt((d_p['r_ankle'][0]-d_p['r_knee'][0])**2+(d_p['r_ankle'][1]-d_p['r_knee'][1])**2)+50)
                    # angle_foot_r = 0
                    if d_p['r_knee'][0] == d_p['r_ankle'][0] and d_p['r_knee'][0] < d_p['r_ankle'][0]:
                        angle_foot_r = 0

                    elif d_p['r_knee'][0] > d_p['r_ankle'][0] and d_p['r_knee'][1] < d_p['r_ankle'][1]:
                        angle_foot_r = triangle_angle(d_p['l_knee'][0],d_p['r_knee'][1],d_p['r_ankle'][0],d_p['r_ankle'][1],d_p['r_knee'][0],d_p['r_ankle'][1])
                    elif d_p['r_knee'][0] < d_p['r_ankle'][0] and d_p['l_knee'][1] < d_p['l_ankle'][1]:
                        angle_foot_r = 0 - triangle_angle(d_p['r_knee'][0],d_p['r_knee'][1],d_p['r_ankle'][0],d_p['r_ankle'][1],d_p['r_knee'][0],d_p['r_ankle'][1])
                    else:
                        angle_foot_r = 0
                    dic_data['foot_r'] = {'w': r_foot_w, 'h': r_foot_h, 'x': d_p['r_knee'][0], 'y': d_p['r_knee'][1],'angle': angle_foot_r,'image_data':img_foot_r}
                res.append(dic_data)
            return   jsonify({'humanbodydata':res,'facedata' :result_face_d,'errorinfo':'0'})

def triangle_angle(x1,y1,x2,y2,x3,y3):
    # three Side length
    a = math.sqrt((x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3))
    b = math.sqrt((x1 - x3) * (x1 - x3) + (y1 - y3) * (y1 - y3))
    c = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    # 利用余弦定理计算三个角的角度
    A = math.degrees(math.acos((a * a - b * b - c * c) / (-2 * b * c)))
    B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))
    C = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))
    print("There three angles are", round(A, 2), round(B, 2), round(C, 2))
    return round(A, 2)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)