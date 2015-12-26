# -*- coding: utf-8 -*-
import base64 
import json ,threading,time
import wave,time,urllib,urllib2,os,sys,pyaudio,mp3play
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
    
    def get_voice(self,source, lang="zh"):
        filename = 'a.mp3' 
        fullpath = 'c:/a.mp3'
        get_url = self.build_query_url(source, lang)
        # This may throw an exception
        request = urllib2.Request(get_url)
        request.add_header('User-agent', self.user_agent_string)
        response = urllib2.urlopen(request, timeout=5)
        if 200 != response.code:
            raise ValueError(str(response.code) + ': ' + response.msg)
        with open(fullpath, 'wb') as audio_file:
            audio_file.write(response.read())
        self.playMp3()
        
    def build_query_url(self,source, lang):
        qdict = dict(lan=lang, ie="UTF-8", text=source.encode('utf-8'), spd = 6, vol = 2)
        return self.url_gtts + urllib.urlencode(qdict)
    
    def playMp3(self):
        logger.info( '正在播放。。。。。。')
        mp3 = mp3play.load('c:/a.mp3')
        mp3.play()
        time.sleep(min(300, mp3.seconds()))    
        mp3.stop()