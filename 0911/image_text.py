#coding=utf-8
#基于python的 实现图片文字识别
from PIL import Image
import pytesseract
#上面都是导包，只需要下面这一行就能实现图片文字识别
text=pytesseract.image_to_string(Image.open('./image/test0911_2.jpeg'),lang='chi_sim')
print(text)
