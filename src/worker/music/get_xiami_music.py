#!/usr/bin/env python2 
# coding:utf-8

import urllib2,os,sys
import lxml.html,shutil
import pygame,time,Queue
import mp3play    
from threading import Thread
class DownLoadMusic(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        # 获取配置文件内的配置信息
        print("开始下载音乐。。。")
        config = ""
        if os.path.isfile("setting.config"):
            config = open("setting.config").readlines()
        else:
            print("配置文件[setting.config]不存在")
        # 存放配置信息的字典
        config_dic = {}
        for cfg in config:
            key,value = cfg.split(":")
            config_dic[key.replace("\n","")] = value.replace("\n","")
        
        url = "http://www.xiami.com/chart/data?c=101&type=0&page=1&limit=10&_=1456582894957"
        userAgent = " User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 "
        headers = { 'User-Agent' : userAgent }
        requst = urllib2.Request(url,headers = headers) 
        result = urllib2.urlopen(requst).read()
         
        # 开始获取返回数据的所有歌曲ID
        html_obj = lxml.html.fromstring(result)
         
        # 下载热曲前，先将之前的清空
        if os.path.exists("top10"):
            shutil.rmtree("top10")
        song_href = html_obj.xpath('tr//strong/a/@href')
        for l in song_href[0:int(config_dic.get("top"))]:
            song_id = l.split('/')[2]
            os.system("python worker/music/xiami.py -s " + song_id)
        
        print("下载结束，共下载[%s]首歌曲" % config_dic.get("top"))
    
class PlayMusic(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        print("开始播放音乐。。。")
        # 找到音乐目录的所有文件，进行顺序播放
        mp3_list = Queue.Queue(maxsize = 10)
        # 查询文件夹中所有的音乐文件。
        print(os.listdir("top10"))
        for file in os.listdir("top10"):
            if os.path.isfile("top10"+os.path.sep+file):
                mp3_list.put(os.getcwd() + os.path.sep+"top10"+os.path.sep+file)
        # 初始化播放器
        #pygame.init()
        pygame.mixer.init()
        pygame.time.delay(1000)
        screen=pygame.display.set_mode([640,480])
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        print('11111111111        ' + str(mp3_list.qsize()))
        clock = pygame.time.Clock()
        # 循环播放
        pygame.mixer.music.load(mp3_list.get())
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        #time.sleep(100)
        print(str(mp3_list.qsize()))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #pygame.mixer.music.stop()   
                    running = False
                    #sys.exit()
                    print("exit1")
                    #return
            print('2222222')
            if not pygame.mixer.music.get_busy() and not mp3_list.empty():
            #if not pygame.mixer.music.get_busy() and mp3_list.qsize() > 1:
                print('当前播放列表还有[%s]首音乐。' % mp3_list.qsize())
                next_song = mp3_list.get()
                print('即将播放下一首曲目[%s]' % next_song)
                pygame.mixer.music.queue(next_song)
                pygame.mixer.music.load(next_song)
                pygame.mixer.music.play()
            else:
                print("exit2")
                #pygame.mixer.music.stop()   
                #return
                #sys.exit()
                 