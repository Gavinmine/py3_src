# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from pymongo import MongoClient
from re import compile


class LagouPipeline(object):
    def __inti__(self):
        self.mongoClient = MongoClient("mongodb://lagou:lagou@127.0.0.1:27017/lagoudb")
        self.db = self.mongoClient['lagoudb']
        self.jobs = self.db['db_parse_jobs']
        self.urls = self.db['wrongurls']
        self.expat = compile(r'经验(\d+)-(\d+)年')
        self.edpat = compile(r'(\w+)及以上')

    def process_item(self, item, spider):
        if item['city'] == None or item['description'] == None:
            self.urls.insert(dict(item))
            raise DropItem('Missing city or description in %s' % item)

        try:
            item['name'] = item['name'][0]
        except IndexError:
            raise DropItem('Missing Name in %s' % item)

        try:
            item['salary'] = item['salary'][0]
        except IndexError:
            raise DropItem('Missing Salary in %s' % item)

        item['salary'] = item['salary'].split('-')
        item['salary'] = [i.strip(' ') for i in item['salary']]
        item['salary'] = [i.strip('k') for i in item['salary']]
        item['salary'] = [int(i) for i in item['salary'] if i.isdigit()]

        item['experience'] = item['experience'].strip(' /')
        match = self.expat.match(item['experience'])
        ex = []
        if match:
            ex.append(int(match.group(1)))
            ex.append(int(match.group(2)))
        else:
            ex.append(0)
        item['experience'] = ex

        item['education'] = item['education'].strip(' /')
        match = self.edpat.match(item['education'])
        if match:
            item['education'] = match.group(1)
        else:
            item['education'] = '不限'

        try:
            item['advantage'] = item['advantage'][0]
        except IndexError:
            raise DropItem('Missing advantage in %s' % item)

        item['advantage'] = item['advantage'].split(',')

        self.jobs.insert(dict(item))

        return item

    def close_spider(self, spider):
        self.mongoClient.close()