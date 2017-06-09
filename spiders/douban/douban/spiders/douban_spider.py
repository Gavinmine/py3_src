# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request,FormRequest
from douban.settings import *
from douban.items import DoubanItem
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class doubanSpider(CrawlSpider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = [
            "https://movie.douban.com/subject/26260853/",
            # "https://movie.douban.com/subject/7065334/",
            # "https://movie.douban.com/subject/26748673/",
            # "https://movie.douban.com/subject/26688477/",
            # "https://movie.douban.com/subject/7065335/",
        ]

    rules = (
        # 将所有符合正则表达式的url请求后下载网页代码, 形成response后调用自定义回调函数
        # Rule(LinkExtractor(allow=(r'https://movie\.douban\.com/subject/\d+',)), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=(r'https://movie\.douban\.com/subject/\d+/\?from=subject\-page',)), callback='parse_page', follow=True),
    )


    def parse_page(self, response):
        sel = Selector(response)
        item = DoubanItem()

        item["url"] = response.url
        item["name"] = sel.xpath('//h1/span[@property="v:itemreviewed"]/text()').extract()
        item["votes"] = sel.xpath('//span[@property="v:votes"]/text()').extract()
        item["average"] = sel.xpath('//strong[@property="v:average"]/text()').extract()
        item["directed"] = sel.xpath('//a[@rel="v:directedBy"]/text()').extract()
        item["actor"] = sel.xpath('//a[@rel="v:starring"]/text()').extract()
        item["genre"] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        item["releaseDate"] = sel.xpath('//span[@property="v:initialReleaseDate"]/text()').extract()
        item["runTime"] = sel.xpath('//span[@property="v:runtime"]/text()').extract()
        item["description"] = sel.xpath('//span[@property="v:summary"]/text()').extract()
        item["starts"] = sel.xpath('//span[@class="rating_per"]/text()').extract()
        print("#################Starts:", item["starts"])
        return item

        # url = response.url
        # name = sel.xpath('//h1/span[@property="v:itemreviewed"]/text()').extract()
        # votes = sel.xpath('//span[@property="v:votes"]/text()').extract()
        # average = sel.xpath('//strong[@property="v:average"]/text()').extract()
        # directed = sel.xpath('//a[@rel="v:directedBy"]/text()').extract()
        # actor = sel.xpath('//a[@rel="v:starring"]/text()').extract()
        # genre = sel.xpath('//span[@property="v:genre"]/text()').extract()
        # releaseDate = sel.xpath('//span[@property="v:initialReleaseDate"]/text()').extract()
        # runTime = sel.xpath('//span[@property="v:runtime"]/text()').extract()
        # description = sel.xpath('//span[@property="v:summary"]/text()').extract()
        # starts = sel.xpath('//span[@class="rating_per"]/text()').extract()
        #
        # print("utl:%s" % url)
        # print("Name:%s" % name)
        # print("Votes:%s" % votes)
        # print("Average:%s" % average)
        # print("directed:%s" % directed)
        # print("Actor:%s" % actor)
        # print("Genre:%s" % genre)
        # print("releaseDate:%s" % releaseDate)
        # print("Run Time:%s" % runTime)
        # print("Description:%s" % description)
        # print("Starts:%s" % starts)
