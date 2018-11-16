# 尝试并连接wifi
import pywifi
import sys
import time
from pywifi import *
from . import conf


def deswifi():
    wifi = PyWiFi()  # 创建一个无限对象
    ifaces = wifi.interfaces()[0]  # 取一个无限网卡
    print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    time.sleep(3)  # 缓冲3秒
    profile = conf  # 配置文件
    profile.ssid = "TP-LINK_489"  # wifi名称
    profile.auth = const.AUTH_ASG_OPEN  # 需要密码
    profile.akm.append(const.AKM_TYPE_WPA2SK)  # 加密类型
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile)  # 连接
    time.sleep(10)  # 尝试10秒能否成功连接
    isok = True
    if ifaces.status() == const.IFACE_CONNECTED:
        print("成功连接")
    else:
        print("失败")
    ifaces.disconnect()  # 断开连接
    time.sleep(1)
    return isok


deswifi()
