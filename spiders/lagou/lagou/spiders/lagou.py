# -*- coding: utf-8 -*-

from lagou.items import LagouItem
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# DUTYS = ['岗位职责：\xa0', '工作内容：', '岗位职责：']
# REQUS = ['任职要求：\xa0', '工作要求：', '任职资格：']
# ENDS = ['加入我们你将获得：']

class lagouSpider(CrawlSpider):
    name = "lagou"
    allowed_domains = ['www.lagou.com', 'm.lagou.com']
    start_urls = [
        # 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
        'https://www.lagou.com/jobs/3093768.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=(r'https://www\.lagou\.com/jobs/\d+\.html.*',)), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=(r'https://m\.lagou\.com/jobs/\d+\.html.*',)), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        sel = Selector(response)
        item = LagouItem()

        item['url'] = response.url
        sceew = sel.xpath('//dd[@class="job_request"]/p/span/text()').extract()
        if len(sceew) != 5:
            return item

        description = sel.xpath('//dd[@class="job_bt"]/div/p/text()').extract()
        # print("description:", description)

        all = []
        for d in description:
            try:
                int(d[0])
            except ValueError:
                pass
            else:
                all.append(d)

        last = int(all[-1][0])

        item['name'] = sel.xpath('//div[@class="job-name"]/span[@class="name"]/text()').extract()
        item['salary'] = sel.xpath('//dd[@class="job_request"]/p/span[@class="salary"]/text()').extract()

        item['city'] = sceew[1]
        item['experience'] = sceew[2]
        item['education'] = sceew[3]
        item['workload'] = sceew[4]

        item['labels'] = sel.xpath('//ul[@class="position-label clearfix"]/li/text()').extract()
        item['advantage'] = sel.xpath('//dd[@class="job-advantage"]/p/text()').extract()

        item['description'] = all[0:-last]
        item['requirements'] = all[-last:]
        return item
