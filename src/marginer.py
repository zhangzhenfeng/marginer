# -*- coding: utf-8 -*-
# 录音模块
from recognition.recorder import recorder
# 翻译模块
from recognition.translator import voice2words
import traceback,sys,Queue,os
from network.baiduApi import BaiduApi
from margin.speeker import Speeker

try:
    
    speek = Speeker()
    # 语音反馈
    speek.speek({},"margin,晚上好。")
    # 获取百度语音的token
    baiduApi = BaiduApi()
    baiduApi.init_token()
    token = baiduApi.get_token()
    # 语音队列
    wav_queue=Queue.Queue(1024)
    # 开始工作录音
    recorder.start(wav_queue)
    # 开始音频解析
    voice2words.start(wav_queue,token)
except:
    traceback.print_exc(file=sys.stdout)