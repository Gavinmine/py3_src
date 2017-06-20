#coding:utf-8
import sys
# reload(sys)
# sys.path.append('..')
# sys.setdefaultencoding('utf-8')
from datetime import datetime
import  json
import requests
from lxml import etree
from scrapy.http import FormRequest
from scrapy.selector import  Selector
from scrapy.spiders import CrawlSpider
from urllib.parse import quote
#from items import LagouItem

class Lagouspider(CrawlSpider):
    name='lagouspider'
    city_list=['北京']
    # city_list=['北京','上海','广州','深圳','青岛']
    position_list=['数据分析']
    base_url='https://www.lagou.com/jobs/list_%s?px=default&city=%s'
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


    def get_combine_list(self):
        combine_list=[]
        for position in self.position_list:
            position = quote(position)
            for city in self.city_list:
                dict={}
                city = quote(city)
                url=self.base_url % (position,city)
                postData = {'first': 'true', 'kd': '数据分析', 'pn': '1'}
                html=requests.post(url,headers=self.headers, data=postData).content
                # print('html:',html)
                f = open('data.html', 'w')
                f.write(html.decode('utf-8'))
                f.close()
                selector=etree.HTML(html)
                total_page=selector.xpath('//ul[@id="order"]/li/div[4]/div[3]/span[2]/text()')[0]
                print("City:", city)
                dict['city']=city
                dict['position']=position
                dict['total_page']=total_page
                combine_list.append(dict)
        return combine_list

    def start_requests(self):
        combine_list=self.get_combine_list()
        json_url= 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false'
        for dict in combine_list:
            city=dict['city']
            position=dict['position']
            #转化为整型
            total_page=int(dict['total_page'])
            print(city,position,total_page)
            url=json_url % city
            for page in range(1,total_page+1):
                post_data={"first":"true",
                           'pn':str(page),
                           'kd':position
                }
                yield FormRequest(url,formdata=post_data,cookies=self.cookies,callback=self.parse_json)


    def parse_json(self,response):
        json_data=json.loads(response.text.decode('utf-8'))
        position_data=json_data["content"]["positionResult"]['result']
        for positions in position_data:
            # for i in positions:
            #  print i
            item={}
            position_city=positions['city'].decode()
            createTime=positions['createTime'].decode()
            companyFullName=positions['companyFullName'].decode()
            position=positions['positionName'].decode()
            workYear=positions['workYear'].decode()
            education=positions['education'].decode()
            industryField=positions['industryField'].decode()
            salary=positions['salary'].decode()
            print("industryField", industryField)
            print ("salary:", salary)
            # item[1]=position_city
            # item[2]=createTime
            # item[3]=companyFullName
            # item[4]=position
            # item[5]=workYear
            # item[6]=education
            # item[7]=industryField
            # item[8]=salary
            #遍历出一条数据 调用自己写的类 传递字典 insert 数据
            yield item