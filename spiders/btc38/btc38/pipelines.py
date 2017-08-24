# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from pymongo import MongoClient


class Btc38Pipeline(object):
    def __init__(self):
        self.mongoClient = MongoClient("mongodb://btc38:btc38@127.0.0.1:27017/btc38db")
        self.db = self.mongoClient['btc38db']
        self.market = self.db['coinsmarket']

    def process_item(self, item, spider):
        if item.get('coinName') == None:
            raise DropItem('Can not found coin name')

        self.market.insert(dict(item))

        return item

    def close_spider(self, spider):
        self.mongoClient.close()