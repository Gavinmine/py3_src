import scrapy
from scrapy.http import Request,FormRequest
from douban.settings import *

class doubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["douban.com"]
    start_urls = [
            "https://www.douban.com/subject/26260853/",
            "https://www.douban.com/subject/7065334/"
        ]

    def __init__(self):
        self.headers = HEADER
        self.cookies = COOKIES

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta={'cookiejar': i}, \
                              headers=self.headers, \
                              cookies=self.cookies, \
                              callback=self.parse, \
                              )

    def parse(self, response):
        filename = response.url.split("/")[-2]
        print("filename:%s\n\n\n\n\n\n", filename)
        with open(filename, 'wb') as f:
            f.write(response.body)