# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
from pymongo import MongoClient

class DoubanPipeline(object):
    def __init__(self):
        # self.file = open('douban_items.jl', 'w')
        self.mongoClient = MongoClient("mongodb://douban:douban@127.0.0.1:27017/doubandb")
        self.db = self.mongoClient['doubandb']
        self.coll = self.db['movies']

    def process_item(self, item, spider):
        try:
            item['name'] = item['name'][0]
        except IndexError:
            DropItem('Missing Name in %s' % item)

        try:
            item['votes'] = item['votes'][0]
        except IndexError:
            item['votes'] = 0

        item['votes'] = int(item['votes'])

        try:
            item['average'] = item['average'][0]
        except IndexError:
            item['average'] = 0

        item['average'] = float(item['average'])

        # item['directed'] = item['directed'][0]

        try:
            item['runTime'] = item['runTime'][0]
        except IndexError:
            item['runTime'] = None

        try:
            item['description'] = item['description']
        except IndexError:
            item['description'] = None

        # spider.logger.info('###################save item to local file################################')
        # json.dump(dict(item), self.file)
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line)

        self.coll.insert(dict(item))
        return item

    def close_spider(self, spider):
        # self.file.close()
        self.mongoClient.close()