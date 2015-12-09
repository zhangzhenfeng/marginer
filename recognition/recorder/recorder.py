# -*- coding: utf-8 -*-
from pyaudio import PyAudio,paInt16 
from datetime import datetime 
import wave,Queue
from logger import logger
import threading ,time

class Recorder(threading.Thread):
    def __init__(self, wav_queue):
        threading.Thread.__init__(self)
        #define of params 
        self.NUM_SAMPLES = 2000 
        self.framerate = 8000 
        # 频道
        self.channels = 1 
        self.sampwidth = 2 
        #record time 
        self.TIME = 5
        self.LEVEL=1000
        self.wav_queue=wav_queue
        self.file_name_index=1
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
        logger.info("当前有%s个录音准备翻译" % queue.qsize())
    def record_wave(self):
        #open the input of wave 
        pa = PyAudio() 
        stream = pa.open(format = paInt16, channels = 1, 
        rate = self.framerate, input = True, 
        frames_per_buffer = self.NUM_SAMPLES) 
        save_buffer = [] 
        count = 0 
        while count < self.TIME*2:
            string_audio_data = stream.read(self.NUM_SAMPLES) 
            save_buffer.append(string_audio_data) 
            count += 1 
        
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
            #print filename,'saved'
        else:
            logger.info("文件未保存") 

        save_buffer = []
        stream.close()#在嵌入式设备上必须加这一句，否则只能录音一次，下次录音时提示stram overflow 错误。
        logger.info("录音结束")
def start(wav_queue):
    recorder=Recorder(wav_queue)
    # 父进程结束时，子进程也结束。
    recorder.setDaemon(True)
    recorder.start()
    #recorder.join()