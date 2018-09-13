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
    # 23000000 max
    i = (x+1 for x in range(30000000))

    start_urls.append("https://www.bilibili.com/video/av" + str(next(i)))
    
    custom_settings = {'ITEM_PIPELINES': {'BilibiliRankListSpider.pipelines.TagPipeLine_2':300}}
    #'BilibiliRankListSpider.pipelines.TagPipeLine': 300
    def parse(self, response):
        for each in range(2):
            yield Request("https://www.bilibili.com/video/av" + str(next(self.i)))
        tagName = response.xpath("//li[@class='tag']/a/text()").extract()
        if tagName != []:
            ITEM_NUMBER = len(tagName)
            datetime = response.xpath("//time/text()").extract()[0]
            aid = str(response.url.lstrip('https://www.bilibili.com/video/av').rstrip('/'))
        # 数据装箱
            for i in range(0, ITEM_NUMBER):
                item = BiliTagItem()
                item['tagName'] = tagName[i]
                item['datetime'] = datetime
                item['aid'] = aid
                yield item
