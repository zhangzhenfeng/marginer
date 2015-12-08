# -*- coding: utf-8 -*-
from pyaudio import PyAudio,paInt16 
from datetime import datetime 
import wave,Queue
from logger import logger
import threading ,time

#define of params 
NUM_SAMPLES = 2000 
framerate = 8000 
# 频道
channels = 1 
sampwidth = 2 
#record time 
TIME = 5
LEVEL=1000
mute_count_limit=50
mute_begin=0
mute_end=1
not_mute=0
voice_queue=Queue.Queue(1024)
wav_queue=Queue.Queue(1024)
file_name_index=1
thread_flag=0
start_flag=1
# class RecordThread (threading.Thread) :
#     """docstring for myThread"""
#     def __init__(self):
#         threading.Thread.__init__(self)
# #         name = name
# #         func = func
# #         args = args
#     
#     def run(self):
#         threadLock.acquire()
#         #获得锁之后再运行
#         record_wave('')
#         #释放锁
#         threadLock.release()
class Recorder(threading.Thread):
    def __init__(self, parent = None):
        threading.Thread.__init__(self)
    def run(self):
        print 111
        record_wave()
        print 222
def save_wave_file(filename, data): 
    '''save the date to the wav file''' 
    wf = wave.open(filename, 'wb') 
    wf.setnchannels(channels) 
    wf.setsampwidth(sampwidth) 
    wf.setframerate(framerate) 
    wf.writeframes("".join(data)) 
    wf.close() 
def writeQ(queue,data):
    #     print 'producing object for Q...',
    queue.put(data, 1)
    #     print "size now", queue.qsize()
def record_wave(): 
    print('sdfdfdf')
    logger.info("开始录音")
    #open the input of wave 
    pa = PyAudio() 
    stream = pa.open(format = paInt16, channels = 1, 
    rate = framerate, input = True, 
    frames_per_buffer = NUM_SAMPLES) 
    save_buffer = [] 
    count = 0 
    while count < TIME*2:
        string_audio_data = stream.read(NUM_SAMPLES) 
        save_buffer.append(string_audio_data) 
        count += 1 
    
    save_buffer=save_buffer[:]
    if save_buffer:
        if file_name_index < 11:
            pass
        else:
            file_name_index = 1
        filename = str(file_name_index)+'.wav' 
        save_wave_file(filename=filename, data=save_buffer)  
        writeQ(queue=wav_queue, data=filename)
        file_name_index+=1
        logger.info(filename+"--->saved" ) 
    else:
        logger.info("文件未保存") 

    save_buffer = []  

    stream.close()#在嵌入式设备上必须加这一句，否则只能录音一次，下次录音时提示stram overflow 错误。
    logger.info("录音结束") 
    return filename
def start():
    #threadLock = threading.Lock()
    recorder=Recorder()
    recorder.setDaemon(True)
    recorder.start()