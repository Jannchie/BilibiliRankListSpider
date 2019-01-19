# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliranklistspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    barrage = scrapy.Field()
    play = scrapy.Field()
    pts = scrapy.Field()
    href = scrapy.Field()
    partition = scrapy.Field()
    subPartition = scrapy.Field()
    fans = scrapy.Field()
    submissions = scrapy.Field()

class UserItem(scrapy.Item):
    mid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()

class VideoItem(scrapy.Item):
    aid = scrapy.Field()
    view = scrapy.Field()

class BiliTagItem(scrapy.Item):
    tagName = scrapy.Field()
    datetime = scrapy.Field()
    aid = scrapy.Field()
    channel = scrapy.Field()
    subChannel = scrapy.Field()
    tag = scrapy.Field()

class extraItem(scrapy.Item):
    channel = scrapy.Field()
    aid = scrapy.Field()
    datetime = scrapy.Field()
    author = scrapy.Field()
    view = scrapy.Field()
    favorite = scrapy.Field()
    coin = scrapy.Field()
    share = scrapy.Field()
    like = scrapy.Field()
    danmaku = scrapy.Field()
    dislike = scrapy.Field()
    subChannel = scrapy.Field()
    title = scrapy.Field()

class XiaoheiwuItem(scrapy.Item):
    punishTitle = scrapy.Field()
    punishTypeName = scrapy.Field()
    punishTime = scrapy.Field()
    reasonTypeName = scrapy.Field()
    uid = scrapy.Field()
    uname = scrapy.Field()
    originTypeName = scrapy.Field()
    originUrl = scrapy.Field()
    pid = scrapy.Field()
    blockedType = scrapy.Field()
    blockedDays = scrapy.Field()

class MysqlItem(scrapy.Item):
    data = scrapy.Field()
