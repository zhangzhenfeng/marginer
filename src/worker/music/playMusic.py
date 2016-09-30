# -*- coding: utf-8 -*-
import urllib2,os,sys
import lxml.html,shutil
import pygame,time,Queue
import mp3play    
import platform
from threading import Thread
from util.file_util import *

def playmusic():
    count = 0
    mp3_list = getallMusic()
    print('当前音乐队列长度 -- ' + str(len(mp3_list)))
    if platform.system() != "Windows":
        pygame.mixer.init()
        pygame.time.delay(1000)
        screen=pygame.display.set_mode([640,480])
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        clock = pygame.time.Clock()
        # 循环播放
        mu = mp3_list[count]
        print('即将要播放的音乐'+mu)
        pygame.mixer.music.load(mu)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        #time.sleep(100)
        mp3_status = 'start'
        while True:
            time.sleep(1)
            # 暂停
            if mp3_status == 'stop' and pygame.mixer.music.get_busy() == 1:
                pygame.mixer.music.stop()
                print("暂停播放")
            elif mp3_status == 'start' and pygame.mixer.music.get_busy() != 1:
                pygame.mixer.music.unpause()
                print("开始播放")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    #sys.exit()
            if not pygame.mixer.music.get_busy() and not len(mp3_list) == count:
            #if not pygame.mixer.music.get_busy() and mp3_list.qsize() > 1:
                print('当前播放列表还有[%s]首音乐。' % len(mp3_list))
                next_song = mp3_list[count]
                print('即将播放下一首曲目[%s]' % next_song)
                pygame.mixer.music.queue(next_song)
                pygame.mixer.music.load(next_song)
                pygame.mixer.music.play()
            else:
                #pygame.mixer.music.stop()
                sys.exit()
    else:
        # 如果是windows系统的话，就是用mp3play库
        import mp3play
        mu = mp3_list[count]
        mp3 = mp3play.load(mu) 
        mp3.play()
        while True:
            state = get_config(keys=['state']).get('state')
            #print mp3.ispaused()
            if state == "pause":
                mp3.pause()
            elif state == "stop":
                mp3.stop()
            elif state == "play" and mp3.ispaused():
                mp3.unpause()
            elif state == "next":
                mp3.stop()
                if count < len(mp3_list)-1:
                    count+=1
                    mu = mp3_list[count]
                    mp3 = mp3play.load(mu) 
                    mp3.play()
                    print mu
                    set_config(values={'state':'play'})
            elif state == "last":
                if count > 0:
                    mp3.stop()
                    count-=1
                    mu = mp3_list[count]
                    mp3 = mp3play.load(mu) 
                    mp3.play()
                    print mu
                    set_config(values={'state':'play'})
            elif not mp3.isplaying() and not mp3.ispaused():
                # 如果当前播放完成，自动进行下一曲。
                mp3.stop()
                count+=1
                mu = mp3_list[count]
                mp3 = mp3play.load(mu) 
                mp3.play()
                print mu
                set_config(values={'state':'play'})
            time.sleep(1)
def getallMusic():
    # 找到音乐目录的所有文件，进行顺序播放
    #mp3_list = Queue.Queue(maxsize = 10)
    mp3_list = []
    # 查询文件夹中所有的音乐文件。
    for file in os.listdir("top10"):
        if os.path.isfile("top10"+os.path.sep+file):
            mp3_list.append(os.getcwd() + os.path.sep+"top10"+os.path.sep+file)
    # 初始化播放器
    #pygame.init()
    
    return mp3_list
if __name__ == '__main__':
    playmusic()
    