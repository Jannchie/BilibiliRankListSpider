#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import UserItem
import time
import json


class TagSpider(scrapy.spiders.Spider):
    name = "tagSpider"
    allowed_domains = ["bilibili.com"]

    start_urls = [
    ]
    # 23000000 max
    i = (x+1 for x in range(90000000))
    
    start_urls.append("https://space.bilibili.com/"+str(next(i))+"/#/video")
    
    custom_settings = {'ITEM_PIPELINES': {}}
    #'BilibiliRankListSpider.pipelines.TagPipeLine': 300
    def parse(self, response):
        for each in range(2):
            yield Request()
        tagName = response.xpath("//li[@class='tag']/a/text()").extract()
        if tagName != []:
            ITEM_NUMBER = len(tagName)
            datetime = response.xpath("//time/text()").extract()[0]
            
        # 数据装箱
            for i in range(0, ITEM_NUMBER):
                item = UserItem()
                item['tagName'] = tagName[i]
                item['datetime'] = datetime
                yield item
