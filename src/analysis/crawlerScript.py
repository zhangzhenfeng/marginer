# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from tutorial.spiders.marginer_spider import FollowAllSpider

def spider_working(url='https://zh.wikipedia.org/wiki/%E5%9C%9F%E8%B1%86%E7%BD%91'):
    spider = FollowAllSpider(domain=url)
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(spider)
    # 线程阻塞，爬完之后自己结束线程。
    process.start()