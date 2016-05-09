# -*- coding: utf-8 -*-
import urllib2,os,sys
import lxml.html,shutil
import pygame,time,Queue
import mp3play    
from threading import Thread
def playmusic():
    print("开始播放音乐。。。")
    # 找到音乐目录的所有文件，进行顺序播放
    mp3_list = Queue.Queue(maxsize = 10)
    # 查询文件夹中所有的音乐文件。
    print(os.listdir("top10"))
    for file in os.listdir("top10"):
        if os.path.isfile("top10"+os.path.sep+file):
            mp3_list.put(os.getcwd() + os.path.sep+"top10"+os.path.sep+file)
    # 初始化播放器
    #pygame.init()
    pygame.mixer.init()
    pygame.time.delay(1000)
    screen=pygame.display.set_mode([640,480])
    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
    print('11111111111        ' + str(mp3_list.qsize()))
    clock = pygame.time.Clock()
    # 循环播放
    pygame.mixer.music.load(mp3_list.get())
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)
    #time.sleep(100)
    print(str(mp3_list.qsize()))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                #sys.exit()
        if not pygame.mixer.music.get_busy() and not mp3_list.empty():
        #if not pygame.mixer.music.get_busy() and mp3_list.qsize() > 1:
            print('当前播放列表还有[%s]首音乐。' % mp3_list.qsize())
            next_song = mp3_list.get()
            print('即将播放下一首曲目[%s]' % next_song)
            pygame.mixer.music.queue(next_song)
            pygame.mixer.music.load(next_song)
            pygame.mixer.music.play()
        else:
            #pygame.mixer.music.stop()
            sys.exit()
if __name__ == '__main__':
    playmusic()
    