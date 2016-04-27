# -*- coding: utf-8 -*-
# 录音模块
from recognition.recorder import recorder
from analysis.analysiser import Analysiser
from logger import logger
# 翻译模块
from recognition.translator import voice2words
import traceback,sys,Queue,os
from network.baiduApi import BaiduApi
from margin.speeker import Speeker
#from analysis.crawlerScript import spider_working
from queue import *
from multiprocessing import Process

# 语音队列
wav_queue=Queue.Queue(1024)

def user_terminal():
    logger.info("现在我可以接受文字输入了。")
    flag=True
    while flag: 
        command = raw_input('>>')
        analysiser = Analysiser()
        if command == 'exit':
            flag = False
        else:
            analysiser.do(command)
            
try:
    speek = Speeker()
    # 语音反馈
    #speek.speek({},u"margin,晚上好。")
    # 获取百度语音的token
    baiduApi = BaiduApi()
    baiduApi.init_token()
    token = baiduApi.get_token()
    # 开始工作录音
    recorder.start(wav_queue)
    # 开始音频解析
    voice2words.start(wav_queue,token)
    # 开启输入模式，可以同时支持语音输入和终端输入
    user_terminal()
except:
    traceback.print_exc(file=sys.stdout)
