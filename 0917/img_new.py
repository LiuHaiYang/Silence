from flask import Flask,request
from PIL import Image
from urllib.request import urlopen
import numpy as np
import requests
from flask.ext.restful import Api, Resource
import http.client
app = Flask(__name__)
api = Api(app)


class ImageAPI(Resource):
    def post(self):
        data = request.json
        background_url = data["background"]
        background=urlopen(background_url)
        img_ditu = Image.open(background)
        for item in data['icons']:
            icon_url = item
            icon=urlopen(icon_url)
            img_new = Image.open(icon)
            x = data['icons'][item]['x']
            y = data['icons'][item]['y'] 
            print(item,':',x,'+',y)
            img_new.thumbnail((70,40))
            source = img_new.convert('RGB')
            img_ditu.paste(source,(x,y),mask=img_new)
        img_ditu.save('img.jpg')

        # conn = http.client.HTTPConnection("172.16.25.30:8080")

        # payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=file; filename=open('../Img/ditu.png')\r\nContent-Type: false\r\n\r\n\r\n-----011000010111000001101001--"

        # headers = {
        #     'content-type': "multipart/form-data; boundary=---011000010111000001101001",
        #     'cache-control': "no-cache",
        #     'postman-token': "08964ef0-45fe-1bcc-71a9-be5eec7e00ac"
        #     }
        # files = {'file':('img.jpg',open('img.jpg','rb'))}
        # conn.request("POST", "/upload_picture/v1.0/upload", files=files)
        # res = conn.getresponse()
        # data = res.read()
        # print(data.decode("utf-8"))
        # url = data.decode("utf-8")
        # return url

        url = 'http://172.16.25.30:8080/upload_picture/v1.0/upload'
        files = {'file':('img.jpg',open('img.jpg','rb'))}
        r = requests.post(url,files=files)
        # res = conn.getresponse()
        # data = res.read()
        # # print(data.decode("utf-8"))
        # url = data.decode("utf-8")
        # return url
        print(r.text)
        url = r.text
        return url


api.add_resource(ImageAPI, '/image/')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)







