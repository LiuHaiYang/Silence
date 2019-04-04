# encoding:utf-8
from PIL import Image, ImageDraw
import requests
import os
from flask import Flask, request,render_template
from werkzeug.utils import secure_filename
import uuid
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
            for d_p in data_p:
                drawAvatar.line([d_p['head'][0],d_p['head'][1] , d_p['neck'][0],d_p['neck'][1]],   fill = (255, 100, 0), width = 5) # head-->neck

                drawAvatar.line([d_p['neck'][0],d_p['neck'][1] , d_p['l_shoulder'][0],d_p['l_shoulder'][1]],   fill = (255, 100, 0), width = 5) # neck-->l_shoulder
                drawAvatar.line([d_p['neck'][0],d_p['neck'][1] , d_p['r_shoulder'][0],d_p['r_shoulder'][1]],   fill = (255, 100, 0), width = 5) #neck--->r_shoulder

                drawAvatar.line([d_p['l_shoulder'][0],d_p['l_shoulder'][1] , d_p['l_elbow'][0],d_p['l_elbow'][1]],   fill = (255, 100, 0), width = 5)   #l_shoulder-->l_elbow
                drawAvatar.line([d_p['r_shoulder'][0],d_p['r_shoulder'][1] , d_p['r_elbow'][0],d_p['r_elbow'][1]],   fill = (255, 100, 0), width = 5)   # r_shoulder --> r_elbow

                drawAvatar.line([d_p['l_elbow'][0],d_p['l_elbow'][1] , d_p['l_wrist'][0],d_p['l_wrist'][1]],   fill = (255, 100, 0), width = 5)   #l_elbow --> l_wrist
                drawAvatar.line([d_p['r_elbow'][0],d_p['r_elbow'][1] , d_p['r_wrist'][0],d_p['r_wrist'][1]],   fill = (255, 100, 0), width = 5)   # r_elbow --> r_wrist

                drawAvatar.line([ d_p['neck'][0],d_p['neck'][1] , d_p['l_hip'][0],d_p['l_hip'][1]],   fill = (255, 100, 0), width = 5)    # neck --> l_hip
                drawAvatar.line([ d_p['neck'][0],d_p['neck'][1] , d_p['r_hip'][0],d_p['r_hip'][1]],   fill = (255, 100, 0), width = 5)    #  neck---> r_hip

                drawAvatar.line([d_p['l_hip'][0],d_p['l_hip'][1] , d_p['l_knee'][0],d_p['l_knee'][1]],   fill = (255, 100, 0), width = 5)     # l_hip --> l_knee
                drawAvatar.line([ d_p['r_hip'][0],d_p['r_hip'][1] , d_p['r_knee'][0],d_p['r_knee'][1]],   fill = (255, 100, 0), width = 5)     # r_hip --> r_knee

                drawAvatar.line([ d_p['l_knee'][0],d_p['l_knee'][1] , d_p['l_ankle'][0],d_p['l_ankle'][1]],   fill = (255, 100, 0), width = 5)     # l_knee -->l_ankle
                drawAvatar.line([d_p['r_knee'][0],d_p['r_knee'][1] , d_p['r_ankle'][0],d_p['r_ankle'][1]],   fill = (255, 100, 0), width = 5)     # r_knee  --> r_ankle

            del drawAvatar

            avatar.show()
            return 1
            # avatar.save('./imageuploads_r/'+file_name)
            # with open('./imageuploads_r/'+file_name,'rb') as f :
            #     image_data = f.read()
            #     base64_data = base64.b64encode(image_data)  # 使用 base64 编码
            # return base64_data
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)