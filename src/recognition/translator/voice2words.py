# -*- coding: utf-8 -*-
import base64 
import json ,threading
import wave,time
from logger import logger
from network.baiduApi import BaiduApi
from analysis.analysiser import Analysiser
from network.httpRequest import HttpRequest

class Translator (threading.Thread) :
    def __init__(self):
        pass
    """docstring for myThread"""
    def __init__(self,wav_queue,token):
        #logger.info("初始化【Translator】")
        threading.Thread.__init__(self)
        self.wav_queue = wav_queue
        self.token = token
        print token
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
            content = buf.get('result')[0]
            logger.info(('margin : ' + content).encode('utf8'))
            # 将识别的内容交给【语义理解模块】
            analysiser = Analysiser()
            analysiser.do(content)
        else:
            pass
    
    def readQ(self,queue):
        val = queue.get(1)
        return val
    
def start(wav_queue,token):
    """
    # 开启【语音】->【文字】翻译线程
    """
    translator=Translator(wav_queue,token)
    # 父进程结束时，子进程也结束。
    translator.setDaemon(True)
    translator.start()
    #translator.join()