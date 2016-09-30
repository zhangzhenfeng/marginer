# -*- coding: utf-8 -*-n()
from logger import logger
from margin.speeker import Speeker
"""
    scene场景模块是识别用户当前语意场景
         首先会判断要交给百度语音识别处理还是本地处理
"""
class Scene():
    def __init__(self):
        self.speek = Speeker()
        #logger.info("初始化【Scene】")
    def get_scene(self,content):
        """
        # 获取会话场景
        # content 当前会话语句
        """
        scene_local = True # 标示是否为本地场景
        scene_code  = ""   # 标示场景关键字
        local_keyword = {'音乐':'音乐','室内温度':'室内温度','暂停':'暂停','播放':'播放'}
        if '音乐' in content:
            scene_code = '音乐'
        elif '暂停' in content:
            scene_code = '暂停'
        elif '播放' in content:
            scene_code = '播放'
        elif '下一曲' in content:
            scene_code = '下一曲'
        elif '上一曲' in content:
            scene_code = '上一曲'
        elif '室内温度' in content:
            scene_code = '室内温度'
        elif '原样输出' in content:
            # 调用语音接口，输出语音。
            self.speek.speek({},content.split(':')[1])
        else:
            scene_local = False
        data = {'state':True,'scene_local':scene_local,'code':scene_code}
        return data