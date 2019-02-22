# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LvyouItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    Address = scrapy.Field()
    Grade = scrapy.Field()
    Score = scrapy.Field()
    Price = scrapy.Field()
