# -*- coding: utf-8 -*-
# 上海：https://search.51job.com/list/020000,000000,0000,00,9,99,Python,2,1.html
# 杭州：https://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,1.html
# 北京：https://search.51job.com/list/010000,000000,0000,00,9,99,Python,2,1.html



import scrapy
from ..items import JobItem

class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    # start_urls = ['http://51job.com/']
    place_map = {
        '上海':'020000',
        '杭州':'080200',
        '北京':'010000',
        '郑州':'170200'
    }

    def __init__(self,**kwargs):
        super(A51jobSpider,self).__init__(**kwargs)
        self.place = kwargs.get('place')
        self.place_code = self.place_map[self.place]

    def start_requests(self):
        urls = ['https://search.51job.com/list/{},000000,0000,00,9,99,Python,2,1.html'.format(self.place_code)]
        print('self.place is:', self.place)
        print('self.place_code:',self.place_code)
        for url in urls:
            yield  scrapy.Request(url,callback=self.parse)

    def parse(self,response):
        result_list = response.xpath('//div[@id="resultList"]/div[@class="el"]')
        i = 0
        for result in result_list:
            i += 1
            name = result.xpath('.//p/span/a/text()').extract_first().strip()
            company = result.xpath('.//span[@class="t2"]/a/text()').extract_first().strip()
            money = result.xpath('.//span[@class="t4"]/text()').extract_first().strip()
            address = result.xpath('//span[@class="t3"]/text()').extract()[i]
            item = JobItem()
            item['name'] = name
            item['company'] = company
            item['money'] = money
            item['address'] = address
            yield item

