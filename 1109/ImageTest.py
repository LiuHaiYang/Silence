import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Jakarta Commons-HttpClient/3.1",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Content-Type": "image/jpg",
    "aucode": "",
    "type": 0,
    "keycode": 'f1faa01a298522_',

}
def main(requrl, filePath):
    f = open(filePath,'rb')
    req = requests.post(requrl, files = f, headers = headers)
    resjson = req.json()
    return resjson

if __name__ == '__main__':
    # imageurl = 'upload.erp.360buyimg.local/imageUpload.action'
    imageurl = 'http://upload.erp.360buyimg.local/imageUpload.action'
    filePath = './test.jpg'
    main(imageurl, filePath)