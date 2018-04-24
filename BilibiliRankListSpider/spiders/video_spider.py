#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import VideoItem
import time
import json


class VideoSpider(scrapy.spiders.Spider):
    name = "videoSpider"
    allowed_domains = ["bilibili.com"]
    start_urls = [
        "https://api.bilibili.com/x/web-interface/archive/stat?aid=1"
    ]
    custom_settings = {'ITEM_PIPELINES': {}}

    def parse(self, response):
        j = json.loads(response.body)
        # 数据装箱
        item = VideoItem()
        data = j['data']
        if data != None:

            item['view'] = data['view']
            item['aid'] = data['aid']
            print(item['view'])
            print(item['aid'])
        yield Request(
            "https://api.bilibili.com/x/web-interface/archive/stat?aid=" + str(
                int(
                    response.url.lstrip(
                        'https://api.bilibili.com/x/web-interface/archive/stat?aid='
                    )) + 1),
            callback=self.parse)
