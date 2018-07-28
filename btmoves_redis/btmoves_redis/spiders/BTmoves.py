# -*- coding: utf-8 -*-
# import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import  BtmovesRedisItem
from redis import Redis
from .. import settings

class BtmovesSpider(RedisSpider):
    name = 'BTmoves'
    # allowed_domains = ['www.btbtdy.net']
    # start_urls = ['http://www.btbtdy.net/']
    redis_key = 'btdy:start_urls'

    def __init__(self):
        super().__init__()
        rds = Redis(settings.REDIS_HOST, settings.REDIS_PORT)
        urls = ['http://www.btbtdy.net/btfl/dy30-{}.html'.format(str(page + 1)) for page in range(62)]
        rds.lpush(self.redis_key, *urls)


    def parse(self, response):
        movies = response.xpath('//div[@class="cts_ms"]')
        for movie in movies:
            name = movie.xpath('.//p[@class="title"]/a/text()').extract_first()
            score = movie.xpath('.//p[@class="title"]/span/text()').extract_first()
            category = movie.xpath('.//p[@class="des"]/text()').extract_first()
            item = BtmovesRedisItem()
            item['name'] = name
            item['score'] = score
            item['category'] = category
            yield  item


























