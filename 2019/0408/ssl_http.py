# -*- coding: UTF-8 -*-
import ssl
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import requests
from bs4 import BeautifulSoup

textlist = []
url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
html = requests.get(url)
html.encoding = "utf-8"
#print(html.text)
soup = BeautifulSoup(html.text, "html5lib")  # 解析，创建soup对象
print(soup.prettify())
for i in soup.find_all("a", target="_blank"):  # 利用find_all()方法找到我们要的东西
    textlist.append([i.string, i.get("href")])  # 提取出文字和链接

print("-" * 15 + "\n")
for j in range(1, 11):
    print("\t{0}\t{1}\n".format(j, textlist[j]))  # 格式化输出