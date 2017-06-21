#coding:utf-8

import json
import requests
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from lagou.items import LagouItem

class Lagouspider(CrawlSpider):
    name='lagouspider'
    base_url='https://www.lagou.com/jobs/list_%s?px=default&city=%s'
    jsonUrl = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
    baseJobUrl = "https://www.lagou.com/jobs/%d.html"

    cookies={
        "user_trace_token":"20170409181541-dd5a3f6254e846e0984aa4e2aa76967b",
        "LGUID":"20170409181542-7c9b90ec-1d0d-11e7-bff0-525400f775ce",
        "index_location_city":"%E5%85%A8%E5%9B%BD",
        "JSESSIONID":"ABAAABAAAGGABCB42D674F6A50D472263E4AA3B9CD56192",
        "SEARCH_ID":"576e3bfa5d044f898bf2c4691a10386d",
        "_gid":"GA1.2.320264748.1497966007",
        "_ga":"GA1.2.1882179874.1491732942",
        "LGSID":"20170620214010-fab4e46a-55bd-11e7-ae1c-525400f775ce",
        "LGRID":"20170620220733-ce06a132-55c1-11e7-9d42-5254005c3644",
        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6":"1496410914,1496671002,1497156221,1497616607",
        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6":"1497967651",
        "TG-TRACK-CODE":"search_code"
    }

    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2,de;q=0.2",
        "Connection":"keep-alive",
        "Content-Length":"56",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Host":"www.lagou.com",
        "Origin":"https://www.lagou.com",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "X-Anit-Forge-Code":"0",
        "X-Anit-Forge-Token":"None",
        # "Referer":"https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?px=default&city=%E5%8C%97%E4%BA%AC",
        "X-Requested-With":"XMLHttpRequest"
        }

    def getAllJobsInfo(self):
        postData = {'first': 'true', 'kd': '数据分析', 'pn': '1'}
        content = requests.post(self.jsonUrl, headers=self.headers, cookies=self.cookies, data=postData).content
        content = content.decode("utf-8")
        jsonData = json.loads(content)
        totalCount = jsonData['content']['positionResult']['totalCount']
        pages = int(totalCount/15)
        return pages


    def start_requests(self):
        pages = self.getAllJobsInfo()
        isFirst = 'true'
        for page in range(1,pages+1):
            postData = {
                'first':isFirst,
                'kd':'数据分析',
                'pn':str(page)
            }
            content = requests.post(self.jsonUrl, headers=self.headers, cookies=self.cookies, data=postData).content
            content = content.decode("utf-8")
            jsonData = json.loads(content)
            jobs = jsonData['content']['positionResult']['result']
            isFirst = 'false'
            for job in jobs:
                positionId = job['positionId']
                jobUrl = self.baseJobUrl % positionId
                yield FormRequest(jobUrl, callback=self.parseJson)


    def parseJson(self, response):
        sel = Selector(response)
        item = LagouItem()

        item['url'] = response.url
        sceew = sel.xpath('//dd[@class="job_request"]/p/span/text()').extract()
        if len(sceew) != 5:
            return item

        description = sel.xpath('//dd[@class="job_bt"]/div/p/text()').extract()
        if not description:
            description = sel.xpath('//dd[@class="job_bt"]/div/p/span/text()').extract()

        # print("description:", description)

        all = []
        for d in description:
            try:
                int(d[0])
            except ValueError:
                pass
            else:
                all.append(d)

        try:
            last = int(all[-1][0])
        except IndexError:
            last = 0

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