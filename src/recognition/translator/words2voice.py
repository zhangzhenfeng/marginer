# -*- coding: utf-8 -*-
import base64 ,uuid, os
import json ,threading,time
import wave,time,urllib,urllib2,os,sys,mp3play
from logger import logger
from network.baiduApi import BaiduApi
from network.httpRequest import HttpRequest

class Voicer (threading.Thread):
    """docstring for myThread"""
    def __init__(self,content):
        #logger.info("初始化【Voicer】")
        threading.Thread.__init__(self)
        self.content = content
        self.httpRequest = HttpRequest()
        
        self.url_gtts = 'http://tts.baidu.com/text2audio?'
        self.user_agent_string = 'Mozilla/5.0'
    def run(self):
        self.get_voice(self.content)
    
    def get_voice(self,source,lang="zh"):
        filename = str(uuid.uuid1()) + '.mp3'
        fullpath = 'c:/' + filename
#         if not os.path.isfile(fullpath):
#             os.mknod(fullpath)
        get_url = self.build_query_url(source, lang)
        # This may throw an exception
        request = urllib2.Request(get_url)
        request.add_header('User-agent', self.user_agent_string)
        response = urllib2.urlopen(request, timeout=5)
        if 200 != response.code:
            raise ValueError(str(response.code) + ': ' + response.msg)
        with open(fullpath, 'wb') as audio_file:
            audio_file.write(response.read())
        self.playMp3(fullpath)
        
    def build_query_url(self,source, lang):
        qdict = dict(lan=lang, ie="UTF-8", text=source.encode('utf-8'), spd = 6, vol = 2)
        return self.url_gtts + urllib.urlencode(qdict)
    
    def playMp3(self,fullpath):
        mp3 = mp3play.load(fullpath)
        mp3.play()
        time.sleep(min(300, mp3.seconds()))    
        mp3.stop()
        # 删除文件
        os.remove(fullpath)
        