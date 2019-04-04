# 代码判断是否有无限网卡
import pywifi
import sys
import time
from pywifi import *


def gic():
    wifi = PyWiFi()  # 创建一个无线对象wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]  # 取第一个无限网卡
    if ifaces in [const.IFACE_DISCONNECTED,
                  const.IFACE_INACTIVE]:
        print('已连接')
    else:
        print('未连接')

gic()