# -*- coding: utf-8 -*-
from pyaudio import PyAudio,paInt16 
from datetime import datetime 
import wave
from logger import logger

#define of params 
NUM_SAMPLES = 2000 
framerate = 8000 
# 频道
channels = 1 
sampwidth = 2 
#record time 
TIME = 5 
def save_wave_file(filename, data): 
    '''save the date to the wav file''' 
    wf = wave.open(filename, 'wb') 
    wf.setnchannels(channels) 
    wf.setsampwidth(sampwidth) 
    wf.setframerate(framerate) 
    wf.writeframes("".join(data)) 
    wf.close() 

def record_wave(): 
    logger.info("开始录音")
    #open the input of wave 
    pa = PyAudio() 
    stream = pa.open(format = paInt16, channels = 1, 
    rate = framerate, input = True, 
    frames_per_buffer = NUM_SAMPLES) 
    save_buffer = [] 
    count = 0 
    while count < TIME*2:
        #read NUM_SAMPLES sampling data 
        string_audio_data = stream.read(NUM_SAMPLES) 
        save_buffer.append(string_audio_data) 
        count += 1 
    
    filename = '1.wav'
    save_wave_file(filename, save_buffer) 
    logger.info("录音结束") 
    return filename