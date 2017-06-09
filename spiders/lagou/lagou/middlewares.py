# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, exceptions
import random
from lagou.settings import USER_AGENTS


class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def __init__(self):
        self.user_agents = USER_AGENTS

    # @classmethod
    def process_request(self, request, spider):
        self.user_agent = random.choice(self.user_agents)
        request.headers.setdefault('User-Agent', self.user_agent)


    def process_response(self, request, response, spider):
        spider.logger.info("status:%d" % response.status)
        if response.status == 200:
            return response
        elif response.status == 404:
            spider.logger.info("%s cannot found" % response.url)
            raise exceptions.IgnoreRequest
        elif response.status == 403:
            spider.logger.info("This user_agent %s has been blocked, remove it and request again" % self.user_agent)
            try:
                self.user_agents.remove(self.user_agent)
            except ValueError:
                spider.logger.info("use agent has already removed, try again")
            return request
        else:
            raise exceptions.IgnoreRequest