# -*- coding: utf-8 -*-
import base64 
import json ,threading
import wave,time
from logger import logger
from network.baiduApi import BaiduApi
from network.httpRequest import HttpRequest
from analysis.analysiser import Analysiser

class Translator (threading.Thread) :
    """docstring for myThread"""
    def __init__(self,wav_queue,token):
        logger.info("初始化Translator")
        threading.Thread.__init__(self)
        self.wav_queue = wav_queue
        self.token = token
    def run(self):
        self.use_cloud(self.token)
        
    ## post audio to server 
    def use_cloud(self,token):
        # 获取http服务
        httpRequest = HttpRequest()
        while True:
            time.sleep(0.5)
            if self.wav_queue.qsize():
                filename=self.readQ(queue=self.wav_queue)
                #logger.info('正在解析[%s]' % filename)
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
            # 进行翻译
            httpRequest.send(srv_url=srv_url,http_header=http_header,call_back_func=self.call_back_func,
                             data=audio_data,data_len=f_len)
            
    def call_back_func(self,buf): 
        buf = json.loads(buf)
        if buf.get('result'):
            print 'margin : ' + buf.get('result')[0]
            # 将识别的内容交给【语义理解模块】
            analysiser = Analysiser()
            analysiser.do()
        else:
            pass
    
    def readQ(self,queue):
        val = queue.get(1)
        return val
    
class Voicer (threading.Thread):
    """docstring for myThread"""
    def __init__(self):
        logger.info("初始化Voicer")
        threading.Thread.__init__(self,content)
        self.content = content
        
    def run(self):
        self.get_voice(self.content)
        
    def voice_back(self,buf):
        print '================='
        print buf
    
    def get_voice(self,content):
        """
        # content  文字
        """
        cuid = "xxxxxxxxxx" #my xiaomi phone MAC 
        srv_url = 'http://tsn.baidu.com/text2audio'
        token = BaiduApi().get_token()
        data = '?tex=' + content + '&lan=zh' + '&tok=' + token + '&ctp=1' + '&cuid=' + cuid
        data_len = len(data)
        http_header = [ 
        'Content-Type: text/xml;', 
        'Content-Length: %d' % data_len
        ] 
        # 进行翻译
        httpRequest.send(srv_url=srv_url,http_header=http_header,call_back_func=self.voice_back,
                         data=data,data_len=data_len)
     
def start(wav_queue,token):
    translator=Translator(wav_queue,token)
    # 父进程结束时，子进程也结束。
    translator.setDaemon(True)
    translator.start()
    translator.join()