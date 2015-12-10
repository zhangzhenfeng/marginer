# -*- coding: utf-8 -*-n()
from logger import logger

class Scene():
    def __init__(self):
        logger.info("初始化场景模块")
    def get_scene(self,content):
        """
        # 获取会话场景
        # content 当前会话语句
        """
        data = {'state':True,'scene':'玩笑'}
        return data