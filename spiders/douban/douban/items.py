# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    votes = scrapy.Field()
    average = scrapy.Field()
    directed = scrapy.Field()
    # script = scrapy.Field()
    actor = scrapy.Field()
    genre = scrapy.Field()
    releaseDate = scrapy.Field()
    runTime = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    starts = scrapy.Field()