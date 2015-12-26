# -*- coding: utf-8 -*-n()
from logger import logger

class Scene():
    def __init__(self):
        pass
        #logger.info("初始化【Scene】")
    def get_scene(self,content):
        """
        # 获取会话场景
        # content 当前会话语句
        """
        data = {'state':True,'scene':'玩笑'}
        return data