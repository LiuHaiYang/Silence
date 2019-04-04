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
            filename = secure_filename(file.filename)
            file_name = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
            sourceFileName = './imageuploads/' + str(file_name)
            avatar  = Image.open(sourceFileName)
            drawAvatar  = ImageDraw.Draw(avatar)
            # url=""
            url=""
            img = open(sourceFileName, 'rb')
            f={"image":img}
            d={"muti_det":2,"url":''}
            r = requests.post( url, files=f, data=d)
            print(r.json())
            data_p = []
            try:
                for i in r.json()['det_info']:
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
                #dic_data = {'head':{'h':50,'w':40,'x':200,'y':100,'angle':15,'image_data':img_head},}
                # 头部的宽高
                head_w, head_h = int(d_p['neck'][1]) - int(d_p['head'][1]), int(d_p['neck'][1]) - int(d_p['head'][1])
                angle_head = 0
                dic_data['head']={'w':head_w,'h':head_h,'x':d_p['head'][0] - 70,'y':d_p['head'][1] - 60,'angle':angle_head,'image_data':img_head}

                # 身体的宽高
                body_w, body_h = d_p['l_shoulder'][0] - d_p['r_shoulder'][0] + 50, d_p['l_hip'][1] - d_p['neck'][1]
                angle_body = 0
                dic_data['body'] = {'w': body_w, 'h': body_h, 'x':d_p['r_shoulder'][0] - 55, 'y': d_p['r_shoulder'][1] - 30,'angle': angle_body,'image_data':img_body}  #d_p['r_shoulder'][0] - 55, d_p['r_shoulder'][1] - 30

                # 胳膊的宽高
                arm_x = (d_p['l_elbow'][1] - d_p['l_shoulder'][1]) ** 2
                arm_y = (d_p['l_shoulder'][0] - d_p['l_elbow'][0]) ** 2
                l_arm_w, l_arm_h = 30, int(numpy.sqrt( arm_x+arm_y ))
                angle_arm_l = 15
                dic_data['arm_l'] = {'w': l_arm_w, 'h': l_arm_h,  'x': d_p['l_shoulder'][0]+10,'y': d_p['l_shoulder'][1],'angle': angle_arm_l,'image_data':img_arm_l}  #d_p['r_shoulder'][0]-10, d_p['r_shoulder'][1]

                r_arm_w, r_arm_h = 30, int(numpy.sqrt((d_p['r_elbow'][1]-d_p['r_shoulder'][1])**2 + (d_p['r_shoulder'][0]-d_p['r_elbow'][0])**2))
                angle_arm_r = 15
                dic_data['arm_r'] = {'w': r_arm_w, 'h': r_arm_h,'x':d_p['r_shoulder'][0]-10, 'y': d_p['r_shoulder'][1],'angle': angle_arm_r,'image_data':img_arm_r}  # d_p['l_shoulder'][0]+10, d_p['l_shoulder'][1]

                ## 小胳膊带手的宽高
                r_hand_w, r_hand_h = 30, int(numpy.sqrt(( d_p['r_wrist'][0]-d_p['r_elbow'][0])**2+(d_p['r_wrist'][1]-d_p['r_elbow'][1])**2))+40
                angle_hand_r = 15
                dic_data['hand_r'] = {'w': r_hand_w, 'h': r_hand_h, 'x': d_p['r_elbow'][0],'y': d_p['r_elbow'][1], 'angle': angle_hand_r,'image_data':img_hand_r}  #d_p['l_elbow'][0], d_p['l_elbow'][1]

                l_hand_w, l_hand_h = 30, int(numpy.sqrt(( d_p['l_wrist'][0]-d_p['l_elbow'][0])**2+(d_p['l_wrist'][1]-d_p['l_elbow'][1])**2))+40
                angle_hand_l = 15
                dic_data['hand_l'] = {'w': l_hand_w, 'h': l_hand_h, 'x': d_p['l_elbow'][0], 'y': d_p['l_elbow'][1], 'angle': angle_hand_l,'image_data':img_hand_l}  # d_p['l_elbow'][0], d_p['l_elbow'][1]

                # 大腿的宽高
                l_leg_w, l_leg_h = 30, int(numpy.sqrt((d_p['l_knee'][0]-d_p['l_hip'][0])**2+(d_p['l_knee'][1]-d_p['l_hip'][1])**2))
                angle_leg_l = 5
                dic_data['leg_l'] = {'w': l_leg_w, 'h': l_leg_h, 'x': d_p['l_knee'][0], 'y': d_p['l_knee'][1],'angle': angle_leg_l,'image_data':img_leg_l}  # d_p['l_knee'][0], d_p['l_knee'][1]

                r_leg_w, r_leg_h = 30, int(numpy.sqrt((d_p['r_knee'][0] - d_p['r_hip'][0]) ** 2 + (d_p['r_knee'][1] - d_p['r_hip'][1]) ** 2))
                angle_leg_r = 5
                dic_data['leg_r'] = {'w': r_leg_w, 'h': r_leg_h, 'x': d_p['r_knee'][0], 'y': d_p['r_knee'][1], 'angle': angle_leg_r,'image_data':img_leg_r}  # d_p['l_knee'][0], d_p['l_knee'][1]

                # 小腿 及 脚 的宽高
                l_foot_w, l_foot_h = 30,  int(numpy.sqrt((d_p['l_ankle'][0]-d_p['l_knee'][0])**2+(d_p['l_ankle'][1]-d_p['l_knee'][1])**2)+50)
                angle_foot_l = 0
                dic_data['foot_l'] = {'w': l_foot_w, 'h': l_foot_h, 'x': d_p['l_knee'][0], 'y': d_p['l_knee'][1],'angle': angle_foot_l,'image_data':img_foot_l}  # d_p['r_knee'][0], d_p['r_knee'][1]

                r_foot_w, r_foot_h = 30,  int(numpy.sqrt((d_p['r_ankle'][0]-d_p['r_knee'][0])**2+(d_p['r_ankle'][1]-d_p['r_knee'][1])**2)+50)
                angle_foot_r = 0
                dic_data['foot_r'] = {'w': r_foot_w, 'h': r_foot_h, 'x': d_p['r_knee'][0], 'y': d_p['r_knee'][1],'angle': angle_foot_r,'image_data':img_foot_r}
                res.append(dic_data)
            print(res)
            return   jsonify({'data':res})
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)