# -*- coding: utf-8 -*-n()
import pycurl,urllib
from logger import logger

class HttpRequest():
    def __init__(self):
        pass
        #logger.info('初始化【HttpRequest】')
    def send(self,srv_url = '',http_header = '',call_back_func = None,data = '',data_len = 0,post=1,connecttimeout=30,timeout=30):
#         print '================='
#         print srv_url
        c = pycurl.Curl() 
        # 请求的url
        c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode 
        #c.setopt(c.RETURNTRANSFER, 1) 
        # 设置请求头
        c.setopt(c.HTTPHEADER, http_header) #must be list, not dict
        if post == 1:
            # post请求
            c.setopt(c.POST, post)
            # 发送的内容
            if data:
                c.setopt(c.POSTFIELDS, data)
        else:
            print 'get'
            c.setopt(pycurl.HTTPGET,1) 
        # 超时时间
        c.setopt(c.CONNECTTIMEOUT, connecttimeout) 
        # 超时时间
        c.setopt(c.TIMEOUT, timeout)
        # 输出方式
        c.setopt(c.WRITEFUNCTION, call_back_func) 
        
        # 内容长度
        c.setopt(c.POSTFIELDSIZE, data_len) 
        # 开始请求
        c.perform() #pycurl.perform() has no return val