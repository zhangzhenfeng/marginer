# -*- coding: utf-8 -*-
from logger import logger
from margin.speeker import Speeker
from study.scene.scene import Scene
from crawlerScript import spider_working
import os
from queue import *
"""
# 语义理解模块
"""
class Analysiser():
    def __init__(self):
        logger.info("初始化【Analysiser】")
    def do(self,content):
        """
        # 语义理解主方法
        # content  需要识别的内容
        """
        # todo 将内容交给【分词器】处理，得到语义。
        # 根据分词结果获取当前对话场景
        scene = Scene()
        # 场景
        scener = scene.get_scene(content)
        # 调用【机器反馈模块】给以语音的返回。
        speek = Speeker()
        # 语音反馈
        speek.speek(scener,u"好的，正在为您查询。")
        
        # 通知爬虫开始查找数据
        spider_queue.put("https://zh.wikipedia.org/wiki/%E8%8B%B1%E9%9B%84%E8%81%94%E7%9B%9F")
        