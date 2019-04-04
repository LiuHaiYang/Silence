# encoding:utf-8
from PIL import Image, ImageDraw
import requests
import os
from flask import Flask, request,render_template
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
            # sourceFileName = "./imageuploads/aa.jpg"
            avatar         = Image.open(sourceFileName)
            drawAvatar     = ImageDraw.Draw(avatar)
            url=""
            img = open(sourceFileName, 'rb')
            f={"image":img}
            # d={"muti_det":1,"url":"http://img2.imgtn.bdimg.com/it/u=2889643740,1342397774&fm=200&gp=0.jpg"}
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
            img_head = Image.open('./static/0912/head.png')
            img_body = Image.open('./static/0912/body.png')
            img_leg_l = Image.open('./static/0912/leg_l.png')
            img_leg_r = Image.open('./static/0912/leg_r.png')
            img_foot_l = Image.open('./static/0912/foot_l.png')
            img_foot_r = Image.open('./static/0912/foot_r.png')
            img_arm_r = Image.open('./static/0912/arm_r.png')
            img_arm_l = Image.open('./static/0912/arm_l.png')

            img_hand_r = Image.open('./static/0912/hand_r.png')
            img_hand_l = Image.open('./static/0912/hand_l.png')

            for d_p in data_p:
                # 分离通道
                # 头部的宽高
                head_w, head_h = int(d_p['neck'][1]) - int(d_p['head'][1]), int(d_p['neck'][1]) - int(d_p['head'][1])
                print(head_w, head_h)
                # 身体的宽高
                body_w, body_h = d_p['l_shoulder'][0] - d_p['r_shoulder'][0] + 50, d_p['l_hip'][1] - d_p['neck'][1]
                # print(body_w, body_h)
                # 胳膊的宽高
                arm_x = (d_p['l_elbow'][1] - d_p['l_shoulder'][1]) ** 2
                arm_y = (d_p['l_shoulder'][0] - d_p['l_elbow'][0]) ** 2
                l_arm_w, l_arm_h = 30, int(numpy.sqrt( arm_x+arm_y ))
                # print(l_arm_w,l_arm_h)
                r_arm_w, r_arm_h = 30, int(numpy.sqrt((d_p['r_elbow'][1]-d_p['r_shoulder'][1])**2 + (d_p['r_shoulder'][0]-d_p['r_elbow'][0])**2))
                # print(r_arm_w,r_arm_h)

                ## 小胳膊带手的宽高
                r_hand_w, r_hand_h = 30, int(numpy.sqrt(( d_p['r_wrist'][0]-d_p['r_elbow'][0])**2+(d_p['r_wrist'][1]-d_p['r_elbow'][1])**2))+40
                # print(r_hand_w,r_hand_h)
                l_hand_w, l_hand_h = 30, int(numpy.sqrt(( d_p['r_wrist'][0]-d_p['r_elbow'][0])**2+(d_p['r_wrist'][1]-d_p['r_elbow'][1])**2))+40
                # print(l_hand_w, l_hand_h)

                # 大腿的宽高
                r_leg_w, r_leg_h = 30, int(numpy.sqrt((d_p['r_knee'][0]-d_p['r_hip'][0])**2+(d_p['r_knee'][1]-d_p['r_hip'][1])**2))
                l_leg_w, l_leg_h = 30, int(numpy.sqrt((d_p['l_knee'][0]-d_p['l_hip'][0])**2+(d_p['l_knee'][1]-d_p['l_hip'][1])**2))
                # 小腿 及 脚 的宽高
                l_foot_w, l_foot_h = 30,  int(numpy.sqrt((d_p['l_ankle'][0]-d_p['l_knee'][0])**2+(d_p['l_ankle'][1]-d_p['l_knee'][1])**2)+50)
                r_foot_w, r_foot_h = 30,  int(numpy.sqrt((d_p['r_ankle'][0]-d_p['r_knee'][0])**2+(d_p['r_ankle'][1]-d_p['r_knee'][1])**2)+50)

                # img_head.thumbnail((head_w+60, head_h+60))
                img_head_re = img_head.resize((head_w+30, head_h+60))

                img_body_re = img_body.resize((body_w+60, body_h+40))

                img_hand_l_re = img_hand_l.resize((l_hand_w,l_hand_h+20))
                img_hand_r_re = img_hand_r.resize((r_hand_w,r_hand_h+20))

                img_arm_l_re = img_arm_l.resize((l_arm_w,l_arm_h))
                img_arm_r_re = img_arm_r.resize((r_arm_w,r_arm_h))
                img_leg_r_re = img_leg_r.resize((r_leg_w,r_leg_h))
                img_leg_l_re = img_leg_l.resize((l_leg_w,l_leg_h))

                img_foot_le=img_foot_l.resize((l_foot_w,l_foot_h+30))
                # img_foot_r.thumbnail((r_foot_w,r_foot_h))
                img_foot_re = img_foot_r.resize((r_foot_w,r_foot_h+30))
                if  d_p['head'][1]  > d_p['neck'][1]:
                    pass
                else:
                    avatar.paste(img_head_re, (d_p['head'][0] - 70, d_p['head'][1] - 60), mask=img_head_re)
                    avatar.paste(img_body_re, (d_p['r_shoulder'][0] - 55, d_p['r_shoulder'][1] - 30), mask=img_body_re)
                    # drawAvatar.line([d_p['head'][0],d_p['head'][1] , d_p['neck'][0],d_p['neck'][1]],   fill = (255, 100, 100), width = 5) # head-->neck

                # drawAvatar.line([d_p['neck'][0],d_p['neck'][1] , d_p['l_shoulder'][0],d_p['l_shoulder'][1]],   fill = (255, 100, 0), width = 5) # neck-->l_shoulder
                # drawAvatar.line([d_p['neck'][0],d_p['neck'][1] , d_p['r_shoulder'][0],d_p['r_shoulder'][1]],   fill = (255, 100, 0), width = 5) #neck--->r_shoulder
                #
                # drawAvatar.line([d_p['l_shoulder'][0],d_p['l_shoulder'][1] , d_p['l_elbow'][0],d_p['l_elbow'][1]],   fill = (255, 100, 0), width = 5)   #l_shoulder-->l_elbow
                # drawAvatar.line([d_p['r_shoulder'][0],d_p['r_shoulder'][1] , d_p['r_elbow'][0],d_p['r_elbow'][1]],   fill = (255, 100, 0), width = 5)   # r_shoulder --> r_elbow
                #
                # drawAvatar.line([d_p['l_elbow'][0],d_p['l_elbow'][1] , d_p['l_wrist'][0],d_p['l_wrist'][1]],   fill = (255, 100, 0), width = 5)   #l_elbow --> l_wrist
                # drawAvatar.line([d_p['r_elbow'][0],d_p['r_elbow'][1] , d_p['r_wrist'][0],d_p['r_wrist'][1]],   fill = (255, 100, 0), width = 5)   # r_elbow --> r_wrist
                #
                # drawAvatar.line([ d_p['neck'][0],d_p['neck'][1] , d_p['l_hip'][0],d_p['l_hip'][1]],   fill = (255, 100, 100), width = 5)    # neck --> l_hip
                # drawAvatar.line([ d_p['neck'][0],d_p['neck'][1] , d_p['r_hip'][0],d_p['r_hip'][1]],   fill = (255, 100, 100), width = 5)    #  neck---> r_hip

                if d_p['l_hip'][1] > d_p['l_knee'][1]:
                    pass
                else:
                    img_leg_l_re_rotate = img_leg_r_re.rotate(-15)
                    avatar.paste(img_leg_l_re_rotate, (d_p['l_hip'][0], d_p['l_hip'][1]), mask=img_leg_l_re_rotate)
                    # drawAvatar.line([d_p['l_hip'][0],d_p['l_hip'][1] , d_p['l_knee'][0],d_p['l_knee'][1]],   fill = (255, 100, 0), width = 5)     # l_hip --> l_knee
                if d_p['r_hip'][1] > d_p['r_knee'][1]:
                    pass
                else:
                    img_leg_r_re = img_leg_r.resize((r_leg_w, r_leg_h))
                    # drawAvatar.line([ d_p['r_hip'][0],d_p['r_hip'][1] , d_p['r_knee'][0],d_p['r_knee'][1]],   fill = (255, 100, 0), width = 5)     # r_hip --> r_knee
                if d_p['l_knee'][1] > d_p['l_ankle'][1]:
                    pass
                else:
                    avatar.paste(img_foot_le, (d_p['l_knee'][0], d_p['l_knee'][1]), mask=img_foot_le)
                    # drawAvatar.line([ d_p['l_knee'][0],d_p['l_knee'][1] , d_p['l_ankle'][0],d_p['l_ankle'][1]],   fill = (255, 100, 0), width = 5)     # l_knee -->l_ankle

                if d_p['r_knee'][1] > d_p['r_ankle'][1]:
                    pass
                else:
                    avatar.paste(img_foot_re, (d_p['r_knee'][0], d_p['r_knee'][1]), mask=img_foot_re)
                    # drawAvatar.line([d_p['r_knee'][0],d_p['r_knee'][1] , d_p['r_ankle'][0],d_p['r_ankle'][1]],   fill = (255, 100, 0), width = 5)     # r_knee  --> r_ankle

                avatar.paste(img_leg_r_re,  (d_p['r_hip'][0],d_p['r_hip'][1]),mask=img_leg_r_re)

                img_arm_l_re_rotate = img_arm_l_re.rotate(0)
                img_arm_r_re_rotate = img_arm_r_re.rotate(0)
                avatar.paste(img_arm_l_re_rotate, (d_p['r_shoulder'][0]-10, d_p['r_shoulder'][1]), mask=img_arm_l_re_rotate)
                avatar.paste(img_arm_r_re_rotate, (d_p['l_shoulder'][0]+10, d_p['l_shoulder'][1]), mask=img_arm_r_re_rotate)

                img_hand_l_re_rotate = img_hand_l_re.rotate(-30)
                img_hand_r_re_rotate = img_hand_r_re.rotate(20)

                avatar.paste(img_hand_l_re_rotate, (d_p['l_elbow'][0], d_p['l_elbow'][1]), mask=img_hand_l_re_rotate)
                avatar.paste(img_hand_r_re_rotate, (d_p['r_elbow'][0], d_p['r_elbow'][1]), mask=img_hand_r_re_rotate)

                # avatar.paste(img_new, (0,0),mask=img_new)
            del drawAvatar
            avatar.show()
            avatar.save('./imageuploads_body/'+file_name)
            with open('./imageuploads_body/'+file_name,'rb') as f :
                image_data = f.read()
                base64_data = base64.b64encode(image_data)  # 使用 base64 编码
            return base64_data
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)