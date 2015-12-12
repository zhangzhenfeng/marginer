# -*- coding: utf-8 -*-n()
from logger import logger
from margin.speeker import Speeker
from study.scene.scene import Scene
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
        speek.speek(scener,content)