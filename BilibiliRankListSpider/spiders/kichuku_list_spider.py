#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BilibiliranklistspiderItem
import time


class KichukuSpider(scrapy.spiders.Spider):
    name = "kichukuSpider"
    allowed_domains = ["bilibili.com"]
    start_urls = ["https://www.bilibili.com/ranking/all/119/0/1"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'BilibiliRankListSpider.pipelines.KichukuPipeLine':200
        }
    }

    def parse(self, response):


        selector = response.xpath("//div[@class='content']")
        ITEM_NUMBER = len(selector)

        title = selector.xpath("//a[@class='title']/text()").extract()
        pts = selector.xpath("//div[@class='pts']/div/text()").extract()

        # 数据装箱
        for i in range(0, ITEM_NUMBER):
            item = BilibiliranklistspiderItem()
            item['title'] = title[i]
            # item['play'] = play[i]
            item['pts'] = pts[i]
            yield item
