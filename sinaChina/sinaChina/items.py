# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinachinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    level1 = scrapy.Field()
    level2 = scrapy.Field()
    level3 = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    pass
