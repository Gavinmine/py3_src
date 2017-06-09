# -*- coding: utf-8 -*-

from lagou.items import LagouItem
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

DUTY = '岗位职责：\xa0'
REQU = '任职要求：\xa0'

class lagouSpider(CrawlSpider):
    name = "lagou"
    allowed_domains = ['www.lagou.com']
    start_urls = [
        'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
    ]

    rules = (
        Rule(LinkExtractor(allow=(r'https://www.lagou.com/jobs/3093768.html',)), callback='parse_page', follow=True)
    )

    def parse_page(self, response):
        sel = Selector(response)
        item = LagouItem()

        item['url'] = response.url
        sceew = sel.xpath('//dd[@class="job_request"]/p/span/text()').extract()
        if len(sceew) != 5:
            return item

        description = sel.xpath('//dd[@class="job_bt"]/div/p/text()').extract()
        try:
            dutyIndex = description.index(DUTY)
            requIndex = description.index(REQU)
        except ValueError:
            return item

        item['name'] = sel.xpath('//div[@class="job-name"]/span[@class="name"]/text()').extract()
        item['salary'] = sel.xpath('//dd[@class="job_request"]/p/span[@class="salary"]/text()').extract()

        item['city'] = sceew[1]
        item['experience'] = sceew[2]
        item['education'] = sceew[3]
        item['workload'] = sceew[4]

        item['labels'] = sel.xpath('//ul[@class="position-label clearfix"]/li/text()').extract()
        item['advantage'] = sel.xpath('//dd[@class="job-advantage"]/p/text()').extract()

        item['description'] = description[dutyIndex+1, requIndex]
        item['requirements'] = description[requIndex+1, len(description)]
        return item
