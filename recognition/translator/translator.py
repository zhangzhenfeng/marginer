# -*- coding: utf-8 -*-
import urllib, urllib2, pycurl 
import base64 
import json 
import wave
from logger import logger
def get_token(): 
    apiKey = "Qa6vDpKF8eFiWjXFrC3erMcl" 
    secretKey = "cf8cdca9e7a792919bf24756ce7f9a0a" 
    
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey; 
    
    res = urllib2.urlopen(auth_url) 
    json_data = res.read() 
    return json.loads(json_data)['access_token'] 

def dump_res(buf): 
    logger.info(buf)

## post audio to server 
def use_cloud(filename):
    token = get_token() 
    fp = wave.open(filename, 'rb') 
    nf = fp.getnframes() 
    f_len = nf * 2 
    audio_data = fp.readframes(nf) 

    cuid = "xxxxxxxxxx" #my xiaomi phone MAC 
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token 
    http_header = [ 
    'Content-Type: audio/pcm; rate=8000', 
    'Content-Length: %d' % f_len 
    ] 
    
    c = pycurl.Curl() 
    # 请求的url
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode 
    #c.setopt(c.RETURNTRANSFER, 1) 
    # 设置请求头
    c.setopt(c.HTTPHEADER, http_header) #must be list, not dict
    # post请求
    c.setopt(c.POST, 1) 
    # 超时时间
    c.setopt(c.CONNECTTIMEOUT, 30) 
    # 超时时间
    c.setopt(c.TIMEOUT, 30) 
    # 输出方式
    c.setopt(c.WRITEFUNCTION, dump_res) 
    # 发送的内容
    c.setopt(c.POSTFIELDS, audio_data) 
    # 内容长度
    c.setopt(c.POSTFIELDSIZE, f_len) 
    # 开始请求
    c.perform() #pycurl.perform() has no return val 