#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BiliTagItem
import time
import json


class TagSpider(scrapy.spiders.Spider):
    name = "tagSpider"
    allowed_domains = ["bilibili.com"]

    start_urls = [
    ]
    start_urls.append("https://www.bilibili.com/video/av6689")
        
    

    custom_settings = {'ITEM_PIPELINES': {'BilibiliRankListSpider.pipelines.TagPipeLine': 300}}

    def parse(self, response):

        tagName = response.xpath("//li[@class='tag']/a/text()").extract()
        if tagName != []:
            ITEM_NUMBER = len(tagName)
            datetime = response.xpath("//time/text()").extract()[0]

        # 数据装箱
            for i in range(0, ITEM_NUMBER):
                item = BiliTagItem()
                item['tagName'] = tagName[i]
                item['datetime'] = datetime
                yield item
                
        for i in range(6689, 23000000):
            yield Request(
                "https://www.bilibili.com/video/av" + str(i),
                callback=self.parse)