# -*- coding: utf-8 -*-
import os
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'project.settings')
from scrapy import log, signals, project
from scrapy.xlib.pydispatch import dispatcher
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue
 
class CrawlerScript():
 
    def __init__(self):
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()
        self.items = []
        dispatcher.connect(self._item_passed, signals.item_passed)
 
    def _item_passed(self, item):
        self.items.append(item)
 
    def _crawl(self, queue, spider_name):
        spider = self.crawler.spiders.create(spider_name)
        if spider:
            self.crawler.queue.append_spider(spider)
        self.crawler.start()
        self.crawler.stop()
        queue.put(self.items)
    @classmethod
    def crawl(self, spider):
        queue = Queue()
        p = Process(target=self._crawl, args=(queue, spider,))
        p.start()
        p.join()
        return queue.get(True)