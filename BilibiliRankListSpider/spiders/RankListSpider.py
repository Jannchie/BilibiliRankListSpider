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

        filename = time.strftime("%Y-%m-%d")
        with open('./temp/' + filename, 'wb') as f:
            f.write(response.body)

        titleSelector = response.xpath("//a[@class='title']")
        title = titleSelector.xpath("text()").extract()

        authorSelector = response.xpath("//div[@class='content']//span[@class='data-box']//i[@class='b-icon author']/parent::node()")
        author = authorSelector.xpath("text()").extract()

        viewSelector = response.xpath("//div[@class='content']//span[@class='data-box']//i[@class='b-icon view']/parent::node()")
        view = viewSelector.xpath("text()").extract()

        ptsSelector = response.xpath("//div[@class='pts']/div")
        pts = ptsSelector.xpath("text()").extract()

        for each in zip(title,author,view,pts):
            item = BilibiliranklistspiderItem()
            item['title'] = each[0]
            item['author'] = each[1]
            item['view'] = each[2]
            item['pts'] = each[3]
            yield item