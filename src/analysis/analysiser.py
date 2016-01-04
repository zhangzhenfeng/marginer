# -*- coding: utf-8 -*-
from logger import logger
from margin.speeker import Speeker
from study.scene.scene import Scene
from crawlerScript import spider_working
from network.httpRequest import HttpRequest
import os,json,urllib,urllib2
from queue import *
"""
# 语义理解模块
"""
class Analysiser():
    def __init__(self):
        pass
        #logger.info("初始化【Analysiser】")
    def do(self,content):
        """
        # 语义理解主方法
        # content  需要识别的内容
        """
        # todo 将内容交给【分词器】处理，得到语义。
        # 根据分词结果获取当前对话场景
        scene = Scene()
        # 场景
        scener = scene.get_scene(content)
        # 调用【机器反馈模块】给以语音的返回。
        speek = Speeker()
        # 语音反馈
        speek.speek(scener,u"好的，正在为您查询。")
        
        # 通知爬虫开始查找数据
        #spider_queue.put("https://zh.wikipedia.org/wiki/%E8%8B%B1%E9%9B%84%E8%81%94%E7%9B%9F")
        
        # 请求图灵机器人返回文字
        self.getTulingMsg(content)
        
    def getTulingMsg(self,content):
        if type(content) == unicode:
            content = content.encode('utf8')
        param = {'key':'ddd2439e877ff940133c6fbcc0c33613','info':content,'userid':'eb2edb736'}
        # 获取http服务
        httpRequest = HttpRequest()
        srv_url = 'http://www.tuling123.com/openapi/api?' + urllib.urlencode(param)
#         http_header = [ 
#         'Content-Type: text/html;', 
#         'Content-Length: %d' % len(content)
#         ]
#         print u'开始请求'
#         print srv_url
#         # 进行翻译
#         httpRequest.send(srv_url=srv_url,http_header=http_header,call_back_func=self.tulingCallBack,
#                          data=None,connecttimeout=5,post=0,data_len=len(content))

        request = urllib2.Request(srv_url)
        request.add_header('User-agent', 'Mozilla/5.0')
        response = urllib2.urlopen(request, timeout=5)
        self.tulingCallBack(response.read())
                         
    def tulingCallBack(self,buf):
        buf = json.loads(buf)
        if buf.get('code'):
            # 调用【机器反馈模块】给以语音的返回。
            speek = Speeker()
            code = buf.get('code')
            logger.info(('margin : ' + buf.get('text').encode('utf8')))
            # 将内容说出来
            if code == 100000:
                # 如果是普通文字
                # 语音反馈
                speek.speek({},buf.get('text'))
            elif code == 200000:
                # 如果是链接类的
                speek.speek({},u"已经给你找到了以下内容，内容打印在屏幕上了。")
                logger.info(('margin : ' + buf.get('url')).encode('utf8'))
            elif code == 302000:
                # 如果是新闻类的
                speek.speek({},u"已经给你找到了以下内容。")
                news = [n['article'] for n in buf['list']]
                speek.speek({},str(news))
                
            elif code == 305000:
                # 如果是列车类的
                msg = [buffer.get('text')]
                for buffer in buf.get('list'):
                    msg_ = buffer.get('trainnum') + '，从，' + buffer.get('start') + '，到，' + buffer.get('terminal') + \
                        '，发车时间，' + buffer.get('starttime') + '，到站时间，' + buffer.get('endtime')
                    msg.append(msg_)
                speek.speek({},str(msg))
            elif code == 306000:
                # 如果是航班类的
                msg = [buffer.get('text')]
                for buffer in buf.get('list'):
                    msg_ = buffer.get('flight') + '，起飞时间，' + buffer.get('starttime') + '，到达时间，' + buffer.get('endtime')
                    msg.append(msg_)
                speek.speek({},str(msg))
            elif code == 308000:
                # 如果是菜谱类的
                msg = [buffer.get('text')]
                for buffer in buf.get('list'):
                    msg_ = buffer.get('name') + '，做法为：' + buffer.get('info')
                    msg.append(msg_)
                speek.speek({},str(msg))
        else:
            speek.speek({},u"亲，我不知该做什么事情了。")
        