#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import UserItem
import time
import json


class UserSpider(scrapy.spiders.Spider):
    name = "userSpider"
    allowed_domains = ["bilibili.com"]
    start_urls = ["https://api.bilibili.com/x/web-interface/card?mid=1"]
    custom_settings = {
        'ITEM_PIPELINES': {}
    }

    def parse(self, response):
        data = json.loads(response.body)['data']
        
        # 数据装箱
        item = UserItem()
        item['name'] = data['card']['name']
        item['mid'] = data['card']['mid']
        print(item['name'])
        print(item['mid'])
        if item['mid'] != "1":
            n = response.meta['n']+1
        else:
            n = 2
        yield Request(
            "https://api.bilibili.com/x/web-interface/card?mid=" + str(n),
            meta={'n': n},
            callback=self.parse)
