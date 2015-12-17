# -*- coding: utf-8 -*-

import scrapy
from margin.speeker import Speeker

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://zh.wikipedia.org/wiki/%E5%9C%9F%E8%B1%86%E7%BD%91"
    ]
    
    def parse(self, response):
        msg = response.xpath("//div[@id='mw-content-text']//p//child::text()").extract()
        sperkword = """"""
        for m in msg:
            sperkword += m.encode('gbk', 'ignore')
        print sperkword
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
        speek = Speeker()
        print '开始反馈内容。。。。。。。。。'
        # 语音反馈
        speek.speek({},sperkword)