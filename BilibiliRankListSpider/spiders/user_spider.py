#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BiliTagItem
import time
import json


class UserSpider(scrapy.spiders.Spider):
    name = "userSpider"
    allowed_domains = ["bilibili.com"]

    state = {}
    state['pages_count'] = state.get('pages_count', 0) + 1

    # 23000000 max
    i = (x + 1 for x in range(99999999))

    start_urls = [
        "https://space.bilibili.com/" + str(state['pages_count']) + "/#/video"
    ]

    custom_settings = {'ITEM_PIPELINES': {}}

    #'BilibiliRankListSpider.pipelines.TagPipeLine': 300
    def parse(self, response):

        self.state['pages_count'] = self.state.get('pages_count', 0) + 1
        i = (x + 1
             for x in range(self.state.get('pages_count', 0) + 1, 99999999))

        yield Request(
            "https://space.bilibili.com/" + str(next(i)) + "/#/video")

        aid = str(
            response.url.lstrip('https://www.bilibili.com/video/av').rstrip(
                '/'))
        tagName = response.xpath("//li[@class='tag']/a/text()").extract()
        if tagName != []:
            ITEM_NUMBER = len(tagName)
            datetime = response.xpath("//time/text()").extract()[0]

            # 数据装箱
            for i in range(0, ITEM_NUMBER):
                item = BiliTagItem()
                item['tagName'] = tagName[i]
                item['datetime'] = datetime
                item['aid'] = aid
                yield item
