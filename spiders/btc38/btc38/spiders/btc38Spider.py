import json
import requests
# from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from time import time, ctime, sleep
from random import random, choice
from btc38.settings import HEADER, USER_AGENTS

class btc38Spider(CrawlSpider):
    name = 'btc38'
    headers = HEADER
    userAgents = USER_AGENTS
    baseApiUrl = 'http://www.btc38.com/httpAPI.php'
    getCoinHoldUrl = 'http://www.btc38.com/trade/getCoinHold.php?coinname=%s&n=%0.16f'
    coinMark = ['SYS', 'BTS', 'BCC', 'BTC', 'LTC', 'DOGE', 'ETH', 'ETC', 'XRP', 'XLM', 'NXT', 'ARDR', 'BLK',
                'XEM', 'EMC', 'DASH', 'INF', 'XZC', 'VASH', 'ICS', 'EAC', 'XCN', 'PPC', 'MGC', 'HLB', 'ZCC',
                'XPM', 'NCS', 'YBC', 'MEC', 'WDC', 'QRK', 'RIC', 'TAG', 'TMC']

    coinInfos = {'current':'2cny', 'zeroCny':'2cny_24h', 'amo':'2cny_amo', 'vol':'2cny_vol', 'high':'high', 'low':'low'}

    def start_requests(self):
        while True:
            currentTime = time()
            self.currentDate = ctime(currentTime)
            n = random()
            currentTime = int(currentTime*1000)
            header = self.headers
            userAgent = choice(self.userAgents)
            header['user-agent'] = userAgent
            payload = {'n':n, '_':currentTime}
            res = requests.get(self.baseApiUrl, headers=header, params=payload)
            self.coinMarketInfo = json.loads(res.text)
            print(self.coinMarketInfo)

            for coin in self.coinMark:
                n = random()
                sleep(1)
                completedCoinHolderurl = self.getCoinHoldUrl % (coin, n)
                yield Request(url=completedCoinHolderurl, callback=self.parseJson)

    def parseJson(self, response):
        url = response.url
        print(url)
        coinHolder = json.loads(response.body)
        print(coinHolder)