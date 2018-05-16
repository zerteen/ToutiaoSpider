# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    URL = scrapy.Field()
    Article = scrapy.Field()
    PublishTime = scrapy.Field()
    Sources = scrapy.Field()
    KeyWords = scrapy.Field()
    Comments = scrapy.Field()

