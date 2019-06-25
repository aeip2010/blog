import socket
from json import load
from urllib.request import urlopen
import hashlib
import datetime
from blog import models
# import execjs


#获取本机ip
def get_ip():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"

#获取电脑名称
def get_name():
    return socket.gethostname()

#获取外网IP
def get_realip():
    try:
        my_ip = load(urlopen('http://httpbin.org/ip'))['origin']
    except:
        my_ip = ' '
    # print(my_ip.split(',')[0])
    return my_ip.split(',')[0]

#获取地理位置
def get_address(ip):
    try:
        addr = load(urlopen('http://ip-api.com/json/%s'%ip))['city']
    except:
        addr = ''
    # print(addr)
    return addr

#加密
def hash_code(s, salt='blog'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

#生成加密串
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    print("1111",code)
    models.ConfirmString.objects.create(code=code,user_id = user.id)
    print(code)
    return code

get_address(get_realip())

