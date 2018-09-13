#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BiliTagItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class TagSpiderCrawl(CrawlSpider):
    name = "tagSpiderCrawl"
    allowed_domains = ["bilibili.com"]

    start_urls = []
    start_urls.append("https://www.bilibili.com/")
    start_urls.append("https://www.bilibili.com/v/music/")
    for i in range(1, 10000):
        start_urls.append("https://www.bilibili.com/video/av" + str(i))

    custom_settings = {
        'ITEM_PIPELINES': {
            'BilibiliRankListSpider.pipelines.TagMongoPipeLine': 300
        }
    }

    # state = {}
    # state['pages_count'] = state.get('pages_count', 0) + 1
    # i = (x+1 for x in range(state.get('pages_count', 0) + 1,99999999))


    rules = [
        Rule(LinkExtractor(allow=(r'https://www.bilibili.com/video/av[0-9]*')),callback="item_parse",follow=True)
    ]


    def item_parse(self, response):

        # self.state['pages_count'] = self.state.get('pages_count', 0) + 1
        # i = (x+1 for x in range(self.state.get('pages_count', 0) + 1,99999999))

        aid = str(response.url.lstrip('https://www.bilibili.com/video/av').rstrip('/'))
        tagName = response.xpath("//li[@class='tag']/a/text()").extract()
        if tagName != []:
            ITEM_NUMBER = len(tagName)
            datetime = response.xpath("//time/text()").extract()[0]

            # 数据装箱
            for i in range(0, ITEM_NUMBER):
                item = BiliTagItem()
                item['tagName'] = tagName[i]
                item['datetime'] = datetime
                item['aid'] = aid
                yield item
# scrapy crawl tagSpiderCrawl -s JOBDIR=tagSpiderCrawl-job