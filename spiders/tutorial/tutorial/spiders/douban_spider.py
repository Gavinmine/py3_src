import scrapy

class doubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["move.douban.com"]
    start_urls = [
            "https://movie.douban.com/subject/26260853/",
            "https://movie.douban.com/subject/7065334/"
        ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
