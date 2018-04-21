#coding=utf-8 
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BilibiliranklistspiderItem
import time

class RankListSpider(scrapy.spiders.Spider):
    name = "rankListSpider"
    allowed_domains = ["bilibili.com"]
    start_urls = [
        "https://www.bilibili.com/ranking/all/0/0/30/"
    ]
    def parse(self, response):

        # 文件名设为当日日期
        filename = time.strftime("%Y-%m-%d")
        with open('./temp/' + filename, 'wb') as f:
            f.write(response.body)

        selector = response.xpath("//div[@class='content']")
        ITEM_NUMBER = len(selector)

        title = selector.xpath("//a[@class='title']/text()").extract()
        author = selector.xpath("//span[@class='data-box']//i[@class='b-icon author']/parent::node()/text()").extract()
        view = selector.xpath("//span[@class='data-box']//i[@class='b-icon view']/parent::node()/text()").extract()
        pts = selector.xpath("//div[@class='pts']/div/text()").extract()
        href = selector.xpath("//a[@class='title']/@href").extract()

        # 数据装箱
        for i in range(0,ITEM_NUMBER):
            item = BilibiliranklistspiderItem()
            item['title'] = title[i]
            item['author'] = author[i]
            item['view'] = view[i]
            item['pts'] = pts[i]
            item['href'] = href[i]

            # 为了爬取分区、粉丝数等数据，需要进入每一个视频的详情页面进行抓取
            yield Request("https://"+href[i][2:],meta={'item':item},callback=self.detailParse)

    def detailParse(self, response):
        item = response.meta['item']
        item['partition'] = response.xpath("/html/body/div[2]/div/div[4]/div[1]/div[1]/span[2]/a/text()").extract()[0]
        item['subPartition'] = response.xpath("/html/body/div[2]/div/div[4]/div[1]/div[1]/span[3]/a/text()").extract()[0]
        item['fans'] = response.xpath("/html/body/div[2]/div/div[4]/div[2]/div[2]/div[3]/span[2]/text()").extract()[0][3:]
        item['submissions'] = response.xpath("/html/body/div[2]/div/div[4]/div[2]/div[2]/div[3]/span[1]/text()").extract()[0][3:]
        yield item
