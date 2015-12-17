# -*- coding: utf-8 -*-
from pyaudio import PyAudio,paInt16 
from datetime import datetime 
import wave,Queue
from logger import logger
import threading ,time
import numpy as np

class Recorder(threading.Thread):
    def __init__(self, wav_queue):
        threading.Thread.__init__(self)
        logger.info("初始化【Recorder】")
        #define of params 
        self.NUM_SAMPLES = 2000 
        self.framerate = 8000 
        # 频道
        self.channels = 1 
        self.sampwidth = 2 
        #record time 
        self.TIME = 2
        # 静音阈值，过滤噪音使用
        self.LEVEL=500
        # 一帧数据数据的有效数据，也就是一帧数据中有多少大于LEVEL的数
        self.mute_count_limit=50
        self.wav_queue=wav_queue
        self.file_name_index=1
        # 标记是否是静音
        self.mute_begin=0
        # 静音时长
        self.mute_end=1
        self.not_mute=0
    def run(self):
        while True:
            self.record_wave()
            time.sleep(1)
    def save_wave_file(self,filename, data):
        '''save the date to the wav file''' 
        wf = wave.open(filename, 'wb') 
        wf.setnchannels(self.channels) 
        wf.setsampwidth(self.sampwidth) 
        wf.setframerate(self.framerate) 
        wf.writeframes("".join(data)) 
        wf.close() 
    def writeQ(self,queue,data):
        queue.put(data, 1)
        #logger.info("当前有%s个录音准备翻译" % queue.qsize())
    def record_wave(self):
        #open the input of wave 
        pa = PyAudio() 
        stream = pa.open(format = paInt16, channels = 1, 
        rate = self.framerate, input = True, 
        frames_per_buffer = self.NUM_SAMPLES) 
        save_buffer = [] 
        count = 0 
        while count < self.TIME*5:
            string_audio_data = stream.read(self.NUM_SAMPLES)
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 得到audio_data中大约level的数据个数
            large_sample_count = np.sum( audio_data > self.LEVEL )
            #print large_sample_count
            #print 'mute_begin' + str(self.mute_begin)
            #print 'mute_end' + str(self.mute_end)
            #未开始计时，出现静音
            # 如果一帧数据数据的有效数据小于mute_count_limit，则认为是静音
            if large_sample_count < self.mute_count_limit :
                # 初始化静音计数
                self.mute_begin=1
            else:
                # 如果有声音出现
                save_buffer.append(string_audio_data)  
                # 静音标记为否
                self.mute_begin=0
                # 静音时长为0
                self.mute_end=1
            count += 1
            # 如果静音时长大于5
            if (self.mute_end - self.mute_begin) > 3:
                # 还原变量
                self.mute_begin=0
                # 还原变量
                self.mute_end=1
                # 结束本次从声卡取值，本次录音结束
                break
            # 如果是静音，那么自增静音时长mute_end
            if self.mute_begin:
                self.mute_end+=1  
        
        save_buffer=save_buffer[:]
        if save_buffer:
            if self.file_name_index < 11:
                pass
            else:
                self.file_name_index = 1
            filename = str(self.file_name_index)+'.wav' 
            self.save_wave_file(filename=filename, data=save_buffer)
            self.writeQ(queue=self.wav_queue, data=filename)
            self.file_name_index+=1

        save_buffer = []
        #在嵌入式设备上必须加这一句，否则只能录音一次，下次录音时提示stram overflow 错误。
        stream.close()
        #logger.info("录音结束")
def start(wav_queue):
    recorder=Recorder(wav_queue)
    # 父进程结束时，子进程也结束。
    recorder.setDaemon(True)
    recorder.start()
    #recorder.join()