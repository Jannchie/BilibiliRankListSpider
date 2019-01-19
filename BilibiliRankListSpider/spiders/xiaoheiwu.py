#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import XiaoheiwuItem
import time
import json
import logging
from pymongo import MongoClient


class XiaoheiwuSpider(scrapy.spiders.Spider):
    name = "xiaoheiwu"
    allowed_domains = ["bilibili.com"]

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'BilibiliRankListSpider.pipelines.XiaoheiwuPipeline': 300
        }
    }

    start_aid = 0
    lenth = 99999999




    def start_requests(self):
        i = (x for x in range(0, 2000))
        for each_i in i:
                yield Request(
                    "https://api.bilibili.com/x/credit/blocked/list?jsonp=jsonp&otype=0&ps=20&pn=" + str(each_i))

    def parse(self, response):
        try:
            r = json.loads(response.body)
            d = r["data"]
            for each_data in d:
                item = XiaoheiwuItem()
                item['punishTitle'] = each_data['punishTitle']
                item['pid'] = each_data['id']
                item['punishTypeName'] = each_data['punishTypeName']
                item['punishTime'] = each_data['punishTime']
                item['reasonTypeName'] = each_data['reasonTypeName']
                item['uid'] = each_data['uid']
                item['blockedDays'] = each_data['blockedDays']
                item['uname'] = each_data['uname']
                if each_data['blockedType'] == 1:
                    item['blockedType'] = '风纪仲裁'
                else:
                    item['blockedType'] = '系统制裁'
                item['originTypeName'] = each_data['originTypeName']
                item['originUrl'] = each_data['originUrl']
                yield item

        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)


# scrapy crawl VideoTagSpider -a start_aid=26053983 -a lenth=2000000 -s JOBDIR=tag-07-21 -L INFO
