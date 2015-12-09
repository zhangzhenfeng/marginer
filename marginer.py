# -*- coding: utf-8 -*-
# 录音模块
from recognition.recorder import recorder
# 翻译模块
from recognition.translator import translator
import traceback,sys,Queue
try:
    # 语音队列
    wav_queue=Queue.Queue(1024)
    # 开始工作录音
    recorder.start(wav_queue)
    # 开始音频解析
    translator.start(wav_queue)
except:
    traceback.print_exc(file=sys.stdout)