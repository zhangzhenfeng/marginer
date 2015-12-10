# -*- coding: utf-8 -*-n()
from logger import logger
from recognition.translator.translator import Voicer

class Speeker():
    def __init__(self):
        logger.info("初始化【Speeker】")
    def speek(self,scene,content):
        """
        # 根据场景和文字播放语音
        # scene     场景
        # content   文字
        """
        self.do(content)
    
    def do(self,content):
        """
        # 将文字转换为语音
        # scene     场景
        # content   文字
        """
        voicer = Voicer(content)
        # 父进程结束时，子进程也结束。
        voicer.setDaemon(True)
        voicer.start()
        voicer.join()