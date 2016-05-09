# -*- coding: utf-8 -*-
"""
    处理本地任务
    例如播放音乐，提示室内温湿度，提示今天天气状况
"""
from worker.music.get_xiami_music import DownLoadMusic,PlayMusic
from margin.speeker import Speeker
import os,subprocess,time
import multiprocessing
class LocalWorker():
    def __init__(self):
        self.speeker = Speeker()
    
    def handle(self,scener = {}):
        # scene为场景元素
        if scener.get("code") == "音乐":
            #player = DownLoadMusic()
            #player.setDaemon(True)
            #player.start()
            #player.join()
            #self.speeker.speek({},u"正在为您下载虾米音乐top10")
            p=subprocess.Popen("python worker/music/playMusic.py", shell=True) 
            p.wait()