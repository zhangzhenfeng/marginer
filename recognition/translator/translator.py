# -*- coding: utf-8 -*-
import urllib, urllib2, pycurl 
import base64 
import json ,threading
import wave,time
from logger import logger

class Translator (threading.Thread) :
    """docstring for myThread"""
    def __init__(self,wav_queue):
        threading.Thread.__init__(self)
        self.wav_queue = wav_queue
    def run(self):
        self.use_cloud()
        
    ## post audio to server 
    def use_cloud(self):
        token = self.get_token()
        while True:
            time.sleep(0.5)
            if self.wav_queue.qsize():
                filename=self.readQ(queue=self.wav_queue)
                logger.info('正在解析[%s]' % filename)
            else:
                continue
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
            c.setopt(c.WRITEFUNCTION, self.dump_res) 
            # 发送的内容
            c.setopt(c.POSTFIELDS, audio_data) 
            # 内容长度
            c.setopt(c.POSTFIELDSIZE, f_len) 
            # 开始请求
            c.perform() #pycurl.perform() has no return val
    def get_token(self): 
        apiKey = "Qa6vDpKF8eFiWjXFrC3erMcl" 
        secretKey = "cf8cdca9e7a792919bf24756ce7f9a0a" 
        
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey; 
        
        res = urllib2.urlopen(auth_url) 
        json_data = res.read() 
        return json.loads(json_data)['access_token'] 

    def dump_res(self,buf): 
        #buf = eval(buf)
        #logger.info(str(buf.get('result')))
        logger.info(buf)
        
    def readQ(self,queue):
        val = queue.get(1)
        return val    
def start(wav_queue):
#    translator=TranslatorThread(use_cloud, (),use_cloud.__name__)
#    translator.setDaemon(True)
#    translator.start()
    translator=Translator(wav_queue)
    # 父进程结束时，子进程也结束。
    translator.setDaemon(True)
    translator.start()
    translator.join()