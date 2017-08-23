# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Btc38Item(scrapy.Item):
    # define the fields for your item here like:
    coinName = scrapy.Field()
    date = scrapy.Field()
    currentPrice = scrapy.Field()
    zeroPrice = scrapy.Field()
    increase = scrapy.Field()
    todayLow = scrapy.Field()
    todayHight = scrapy.Field()
    todayAmo = scrapy.Field()
    todayVol = scrapy.Field()
    change24H = scrapy.Field()
    changeWeek = scrapy.Field()
    coinsPerHolders = scrapy.Field()
    holders = scrapy.Field()
    inflow24H = scrapy.Field()
    inflowWeek = scrapy.Field()
    outflow24H = scrapy.Field()
    outflowWeek = scrapy.Field()
    totalCoins = scrapy.Field()
    pass
