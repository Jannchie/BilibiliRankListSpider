#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BilibiliranklistspiderItem
import time


class BangumiSpider(scrapy.spiders.Spider):
    name = "bangumiSpider"
    allowed_domains = ["bilibili.com"]
    start_urls = ["https://www.bilibili.com/ranking/bangumi/13/0/3"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'BilibiliRankListSpider.pipelines.BangumiPipeLine':200
        }
    }

    def parse(self, response):


        selector = response.xpath("//div[@class='content']")
        ITEM_NUMBER = len(selector)

        title = selector.xpath("//a[@class='title']/text()").extract()
        barrage = selector.xpath(
            "//span[@class='data-box']//i[@class='b-icon view']/parent::node()/text()"
        ).extract()
        pts = selector.xpath("//div[@class='pts']/div/text()").extract()
        play = selector.xpath(
            "//span[@class='data-box']//i[@class='b-icon play']/parent::node()/text()"
        ).extract()

        # 数据装箱
        for i in range(0, ITEM_NUMBER):
            item = BilibiliranklistspiderItem()
            item['title'] = title[i]
            item['barrage'] = barrage[i]
            # item['play'] = play[i]
            item['pts'] = pts[i]
            yield item
