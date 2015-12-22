# -*- coding: utf-8 -*-
import Queue,time
from scrapy.crawler import CrawlerProcess
from study.tutorial.spiders.marginer_spider import FollowAllSpider
from queue import *
def spider_working():
    while True:
        time.sleep(1.5)
        print 111111111111111
        print spider_queue.qsize() 
        if spider_queue.qsize():
            url = spider_queue.get(1)
            print 22222222222222
            print url 
            spider = FollowAllSpider(domain=url)
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            })
            
            process.crawl(spider)
            # 线程阻塞，爬完之后自己结束线程。
            process.start()