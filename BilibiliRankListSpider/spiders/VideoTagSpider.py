#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import BiliTagItem
import time
import json
import logging
from pymongo import MongoClient
from dateutil import parser


class VideoTagSpider(scrapy.spiders.Spider):
    name = "VideoTagSpider"
    allowed_domains = ["bilibili.com"]

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'BilibiliRankListSpider.pipelines.TagMongoPipeLine_2': 300
        }
    }

    start_aid = 1
    lenth = 99999999

    # 链接mongoDB
    client = MongoClient('localhost', 27017)

    # 数据库登录需要帐号密码的话
    # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
    db = client['bili_data']  # 获得数据库的句柄
    coll = db['video']  # 获得collection的句柄

    def __init__(self, start_aid=1, lenth=99999999, *args, **kwargs):
        super(VideoTagSpider, self).__init__(*args, **kwargs)
        self.start_aid = int(start_aid)
        self.lenth = int(lenth)

    #'BilibiliRankListSpider.pipelines.TagPipeLine': 300
    def start_requests(self):
        c = self.coll.find({"aid":{"$gt":34536349},"tag": { "$exists": False }},no_cursor_timeout=True).batch_size(500)
        for each in c:
            yield Request("https://www.bilibili.com/video/av" + str(each['aid']))

    def parse(self, response):
        try:
            aid = str(
                response.url.lstrip('https://www.bilibili.com/video/av')
                .rstrip('/'))
            tagName = response.xpath("//li[@class='tag']/a/text()").extract()
            datetime = response.xpath("//time/text()").extract()
            if datetime != []:
                item = BiliTagItem()
                item['aid'] = int(aid)
                channel = response.xpath("//span[2]/a/text()").extract()
                subChannel = response.xpath("//span[3]/a/text()").extract()
                if channel != []:
                    item['channel'] = channel[0]
                if subChannel != []:
                    item['subChannel'] = subChannel[0]
                item['datetime'] = parser.parse(datetime[0])
                item['tag'] = []
                if tagName != []:
                    ITEM_NUMBER = len(tagName)
                    for i in range(0, ITEM_NUMBER):
                        item['tag'].append(tagName[i])
                yield item

        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)


# usage: scrapy crawl VideoTagSpider -a start_aid=26053983 -a lenth=5000000 -s JOBDIR=tag-1500w--2000w -L INFO