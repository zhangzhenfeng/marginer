# -*- coding: utf-8 -*-
# 录音模块1
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
from util.file_util import set_config,get_config
import time
import threading

# 语音队列
wav_queue=Queue.Queue(1024)

def user_terminal():
    logger.info("现在我可以接受文字输入了。")
    flag=True
    while flag: 
        command = raw_input('>>')
        if command == 'exit':
            flag = False
        else:
            #analysiser.do(command)
            translator=Analysiser(command)
            # 父进程结束时，子进程也结束。
            translator.setDaemon(True)
            translator.start()
def http_terminal():
    logger.info("正在接收http请求。\n")
    flag=True
    while flag:
        commond = get_config(keys=['commond']).get('commond')
        set_config(values={'commond':''})
        if commond:
            translator=Analysiser(commond)
            # 父进程结束时，子进程也结束。
            translator.setDaemon(True)
            translator.start()
        time.sleep(0.5)
    
try:
    # 初始化播放器
    
    set_config(values={'state':'play'})
    set_config(values={'commond':''})
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
    # 开始接收指令
    #start_input()
    http_terminal = threading.Thread(target=http_terminal,args=())
    http_terminal.setDaemon(True)
    http_terminal.start()
    # 开启输入模式，可以同时支持语音输入和终端输入
    user_terminal()
except:
    traceback.print_exc(file=sys.stdout)


