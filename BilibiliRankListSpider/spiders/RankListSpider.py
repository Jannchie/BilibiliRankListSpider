#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BilibiliranklistspiderItem
import time


class RankListSpider(scrapy.spiders.Spider):
    name = "rankListSpider"
    allowed_domains = ["bilibili.com"]
    start_urls = ["https://www.bilibili.com/ranking/all/0/0/30/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'BilibiliRankListSpider.pipelines.BilibiliranklistspiderPipeline':
            300,
        }
    }

    def parse(self, response):

        # 文件名设为当日日期
        filename = time.strftime("%Y-%m-%d")
        with open('./temp/' + filename, 'wb') as f:
            f.write(response.body)

        selector = response.xpath("//div[@class='content']")
        ITEM_NUMBER = len(selector)

        title = selector.xpath("//a[@class='title']/text()").extract()
        author = selector.xpath(
            "//span[@class='data-box']//i[@class='b-icon author']/parent::node()/text()"
        ).extract()
        barrage = selector.xpath(
            "//span[@class='data-box']//i[@class='b-icon view']/parent::node()/text()"
        ).extract()
        pts = selector.xpath("//div[@class='pts']/div/text()").extract()
        href = selector.xpath("//a[@class='title']/@href").extract()
        play = selector.xpath(
            "//span[@class='data-box']//i[@class='b-icon play']/parent::node()/text()"
        ).extract()

        # 数据装箱
        for i in range(0, ITEM_NUMBER):
            item = BilibiliranklistspiderItem()
            item['title'] = title[i]
            item['author'] = author[i]
            item['barrage'] = barrage[i]
            # item['play'] = play[i]
            item['pts'] = pts[i]
            item['href'] = href[i]

            # 为了爬取分区、粉丝数等数据，需要进入每一个视频的详情页面进行抓取
            yield Request(
                "https://" + href[i][2:],
                meta={'item': item},
                callback=self.detailParse)

    def detailParse(self, response):
        item = response.meta['item']
        item['partition'] = response.xpath(
            "//span[@class='crumb'][2]/a/text()").extract()[0]
        item['subPartition'] = response.xpath(
            "//span[@class='crumb'][3]/a/text()").extract()[0]
        item['fans'] = response.xpath("//div[3]/span[2]/@title").extract()[0][
            3:]
        item['submissions'] = response.xpath(
            "//div[3]/span[1]/text()").extract()[0][3:]
        yield item

