#coding=utf-8
import scrapy
from scrapy.http import Request
from BilibiliRankListSpider.items import extraItem
import time
import json
import logging
from dateutil import parser
from pymongo import MongoClient


class HighSpeedVideoSpider(scrapy.spiders.Spider):
    name = "adder"
    allowed_domains = ["bilibili.com"]

    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'BilibiliRankListSpider.pipelines.TagMongoPipeLine_3': 300
        }
    }

    start_aid = 0
    lenth = 99999999

    # def __init__(self, start_aid=0, lenth=99999999, *args, **kwargs):
    # super(VideoTagSpider, self).__init__(*args, **kwargs)
    # self.start_aid = int(start_aid)
    # self.lenth = int(lenth)
    # print("开始的av号为:" + start_aid + ",计划抓取的视频个数为：" + lenth)
    #'BilibiliRankListSpider.pipelines.TagPipeLine': 300
    # 链接mongoDB
    client = MongoClient('localhost', 27017)

    # 数据库登录需要帐号密码的话
    # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
    db = client['bili_data']  # 获得数据库的句柄
    coll = db['video']  # 获得collection的句柄
    d = coll.find({'datetime':None})
    print("等待添加日期的数量："+str(d.count()))

    def start_requests(self):
        # while self.d != None:
        #     aid_str = ''
        #     i = 0
        #     for each in self.d:
        #         i += 1
        #         aid_str += str(each['aid']) + ","
        #         if i == 99:
        #             break

        i = (x for x in range(20000000, 999999999))
        while True:
            aid_str = ''
            for j in range(99):
                aid_str += str(next(i))+','
            yield Request("https://api.bilibili.com/x/article/archives?ids=" + aid_str.rstrip(','))

    def parse(self, response):
        try:
            r = json.loads(response.body)
            d = r["data"]
            keys = list(d.keys())
            for each_key in keys:
                aid = d[each_key]['stat']['aid']
                author = d[each_key]['owner']['name']
                view = d[each_key]['stat']['view']
                favorite = d[each_key]['stat']['favorite']
                coin = d[each_key]['stat']['coin']
                share = d[each_key]['stat']['share']
                like = d[each_key]['stat']['like']
                dislike = d[each_key]['stat']['dislike']
                subChannel = d[each_key]['tname']
                title = d[each_key]['title']
                datetime = d[each_key]['pubdate']

                item = extraItem()
                item['aid'] = aid
                item['author'] = author
                item['view'] = view
                item['favorite'] = favorite
                item['coin'] = coin
                item['share'] = share
                item['like'] = like
                item['dislike'] = dislike
                item['title'] = title
                item['subChannel'] = subChannel
                item['datetime'] = datetime
                yield item

        except Exception as error:
            # 出现错误时打印错误日志
            print("在解析时出错")
            print(r)
            print(response.url)
            logging.error(error)


# scrapy crawl VideoTagSpider -a start_aid=26053983 -a lenth=2000000 -s JOBDIR=tag-07-21 -L INFO
