import scrapy
from BilibiliRankListSpider.items import BilibiliranklistspiderItem

class DmozSpider(scrapy.spiders.Spider):
    name = "rankListSpider"
    allowed_domains = ["bilibili.com"]
    start_urls = [
        "https://www.bilibili.com/ranking/all/0/0/30/"
    ]
    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)

        titleSelector = response.xpath("//a[@class='title']")
        title = titleSelector.xpath("text()").extract()

        authorSelector = response.xpath("//div[@class='content']//span[@class='data-box'][1]//i[@class='b-icon author']/parent::node()")
        author = authorSelector.xpath("text()").extract()
        print(title,author)
        # for sel in response.xpath('//ul/li'):
        #     item = BilibiliranklistspiderItem()
        #     item['title'] = sel.xpath('a/text()').extract()
        #     item['link'] = sel.xpath('a/@href').extract()
        #     item['desc'] = sel.xpath('text()').extract()
        #     yield item