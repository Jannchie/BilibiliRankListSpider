import scrapy
from BilibiliRankListSpider.items import BilibiliranklistspiderItem
import time

class DmozSpider(scrapy.spiders.Spider):
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
            yield item