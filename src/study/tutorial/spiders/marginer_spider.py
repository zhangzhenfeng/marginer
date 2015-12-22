# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
import re
from six.moves.urllib.parse import urlparse

import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor

from study.tutorial.items import MarginItem as Page


class FollowAllSpider(scrapy.Spider):

    name = 'marginer'

    def __init__(self, **kw):
        super(FollowAllSpider, self).__init__(**kw)
        url = kw.get('url') or kw.get('domain') or 'https://zh.wikipedia.org/wiki/%E5%9C%9F%E8%B1%86%E7%BD%91'
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        self.url = url
        self.allowed_domains = [re.sub(r'^www\.', '', urlparse(url).hostname)]
        self.link_extractor = LinkExtractor()
        self.cookies_seen = set()

    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        """Parse a PageItem and all requests to follow
        @url http://www.scrapinghub.com/
        @returns items 1 1
        @returns requests 1
        @scrapes url title foo
        """
#        page = self._get_item(response)
#        r = [page]
#        r.extend(self._extract_requests(response))
        msg = response.xpath("//div[@id='mw-content-text']//p//child::text()").extract()
        sperkword = """"""
        for m in msg:
            sperkword += m.encode('gbk', 'ignore') 
        print sperkword
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)

    def _get_item(self, response):
        item = Page(
            url=response.url,
            size=str(len(response.body)),
            referer=response.request.headers.get('Referer'),
        )
        self._set_title(item, response)
        self._set_new_cookies(item, response)
        return item

    def _extract_requests(self, response):
        r = []
        if isinstance(response, HtmlResponse):
            links = self.link_extractor.extract_links(response)
            r.extend(Request(x.url, callback=self.parse) for x in links)
        return r

    def _set_title(self, page, response):
        if isinstance(response, HtmlResponse):
            title = response.xpath("//title/text()").extract()
            if title:
                page['title'] = title[0]

    def _set_new_cookies(self, page, response):
        cookies = []
        for cookie in [x.split(';', 1)[0] for x in
                       response.headers.getlist('Set-Cookie')]:
            if cookie not in self.cookies_seen:
                self.cookies_seen.add(cookie)
                cookies.append(cookie)
        if cookies:
            page['newcookies'] = cookies