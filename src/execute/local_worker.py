# -*- coding: utf-8 -*-
"""
    处理本地任务
    例如播放音乐，提示室内温湿度，提示今天天气状况
"""
from worker.music.get_xiami_music import get_music_from_xiami
from margin.speeker import Speeker
class LocalWorker():
    def __init__(self):
        self.speeker = Speeker()
    def handle(self,scener = {}):
        # scene为场景元素
        if scener.get("code") == "音乐":
            get_music_from_xiami()
            self.speeker.speek({},u"正在为您下载虾米音乐top10")
        