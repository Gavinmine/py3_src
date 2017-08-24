import json
import requests
# from scrapy.http import FormRequest
from scrapy.http import Request
from re import match
# from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from time import time, ctime, sleep
from random import random, choice
from btc38.settings import HEADER, USER_AGENTS
from btc38.items import Btc38Item

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
            # print(self.coinMarketInfo)

            for coin in self.coinMark:
                n = random()
                # sleep(1)
                completedCoinHolderurl = self.getCoinHoldUrl % (coin, n)
                yield Request(url=completedCoinHolderurl, callback=self.parseJson)

            sleep(60)

    def parseJson(self, response):
        item = Btc38Item()
        url = response.url
        m = match(r'http.*coinname=(.*)&.*', url)
        if not m:
            return item
        item['coinName'] = m.group(1)
        item['date'] = response.headers['Date'].decode("utf-8")
        item['currentPrice'] = float(self.coinMarketInfo[item['coinName'].lower() + self.coinInfos['current']])
        item['zeroPrice'] = float(self.coinMarketInfo[item['coinName'].lower() + self.coinInfos['zeroCny']])
        item['increase'] = (item['currentPrice'] - item['zeroPrice']) / item['zeroPrice']
        item['todayLow'] = float(self.coinMarketInfo[item['coinName'].lower() + self.coinInfos['low']])
        item['todayHight'] = float(self.coinMarketInfo[item['coinName'].lower() + self.coinInfos['high']])
        item['todayAmo'] = float(self.coinMarketInfo[item['coinName'].lower() + self.coinInfos['amo']])
        item['todayVol'] = float(self.coinMarketInfo[item['coinName'].lower() + self.coinInfos['vol']])

        coinHolder = json.loads(response.body)
        item['change24H'] = float(coinHolder['change24H'].split(" ")[0])
        item['changeWeek'] = float(coinHolder['changeWeek'].split(" ")[0])
        item['coinsPerHolders'] = coinHolder['coinsPerHolders']
        item['holders'] = coinHolder['holders']
        item['inflow24H'] = float(coinHolder['inflow24H'].split(" ")[0])
        item['inflowWeek'] = float(coinHolder['inflowWeek'].split(" ")[0])
        item['outflow24H'] = float(coinHolder['outflow24H'].split(" ")[0])
        item['outflowWeek'] = float(coinHolder['outflowWeek'].split(" ")[0])
        item['totalCoins'] = coinHolder['totalCoins']

        return item
        # print(url)

        # print(coinHolder)

