# -*- coding: utf-8 -*-
import scrapy
from ..items import LvyouItem
from scrapy import Spider, Request, FormRequest
import re
def xinxi(pre, str):
    try:
        return re.findall(pre, str, re.S)[0]
    except:
        return 'None'

class WenzhouSpider(scrapy.Spider):
    name = 'wenzhoulvyou'
    start_urls = ['http://you.ctrip.com/sight/wenzhou153/s0-p1.html']
    def parse(self, response):
        strs = response.xpath('//div[@class="list_wide_mod2"]/div[@class="list_mod2"]/div[@class="rdetailbox"]').extract()
        item = LvyouItem()
        for str in strs:
            item["Name"] = re.findall(r'title="(.*?)"', str, re.S)[0]
            item["Address"] = re.findall(r'<dd class="ellipsis">(.*?)</dd>', str, re.S)[0]
            item["Grade"] = xinxi(r'[A]+级景区', str)
            item["Score"] = xinxi(r'<li><a class="score" href=".*?"><strong>(.*?)</strong>', str)
            item["Price"] = xinxi(r'<span class="price"><i>¥</i>(.*?)<b class="red">', str)
            yield item
        # 翻页
        for i in reversed(range(2, 128)):
            yield Request("http://you.ctrip.com/sight/Wenzhou153/s0-p{0}.html".format(i), callback=self.parse)




