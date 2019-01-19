# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime
import time
import pymysql
import configparser
from pymongo import InsertOne, DeleteOne, ReplaceOne

# 自己创建的database配置文件，其中包含数据库链接信息。
import logging

# 使用mongoDB
from pymongo import MongoClient


# 单位换算，化为K（千）。
def unit_convert(item):
    if item['barrage'][-1] == u'万':
        item['barrage'] = float(item['barrage'][:-1]) * 10
    else:
        item['barrage'] = float(item['barrage']) / 1000

    #if item['play'][-1] == u'万':
    #    item['play'] = float(item['play'][:-1]) * 10
    #else:
    #    item['play'] = float(item['play']) / 1000


def connect_db():

    cf = configparser.ConfigParser()
    cf.read("db.conf")
    connect = pymysql.connect(
        host='localhost',
        db='bilibili',
        user='jannchie',
        passwd='141421',
        charset='utf8mb4',
        use_unicode=True)
    return connect


class BilibiliranklistspiderPipeline(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        unit_convert(item)
        try:
            # 插入数据
            self.cursor.execute(
                """insert into bilibili_rank_list(title, author, bilibili_rank_list.barrage,play, pts ,href, bilibili_rank_list.partition,bilibili_rank_list.subPartition,author_fans,author_submissions)value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['title'], item['author'], item['barrage'], 0,
                 item['pts'], item['href'], item['partition'],
                 item['subPartition'], item['fans'], item['submissions']))
            # 提交sql语句

            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class ApiMySqlPipeline(object):
    def __init__(self):
        print("初始化ApiMySqlPipeline")
        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        try:
            # 插入数据
            self.cursor.executemany(
                """insert into video(`aid`,`author`,`view`,`favorite`,`danmaku`,`coin`,`share`,`like`,`dislike`,`subchannel`,`title`,`datetime`,`channel`)value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)     
                ON DUPLICATE KEY UPDATE  
                id = 1,  
                name = 'world',  
                age = 55  """, item['data'])
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class DailyRankListPipeLine(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        unit_convert(item)
        try:
            # 插入数据
            self.cursor.execute(
                """insert into bilibili_rank_list_daily(title, author, bilibili_rank_list_daily.barrage,play, pts ,href, bilibili_rank_list_daily.partition,bilibili_rank_list_daily.subPartition,author_fans,author_submissions)value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['title'], item['author'], item['barrage'], 0,
                 item['pts'], item['href'], item['partition'],
                 item['subPartition'], item['fans'], item['submissions']))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class BangumiPipeLine(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """insert into bangumi(title,barrage,play, pts,`date`)value (%s,%s,%s,%s,%s)""",
                (item['title'], item['barrage'], 0, item['pts'],
                 time.strftime('%Y-%m-%d', time.localtime(time.time()))))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class KichukuPipeLine(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """
                insert into kichuku_daily(title, pts,`date`)value (%s,%s,%s)""",
                (item['title'], item['pts'],
                 time.strftime('%Y-%m-%d', time.localtime(time.time()))))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class Kichuku7PipeLine(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """
                insert into kichuku_7(title, pts,`date`)value (%s,%s,%s)""",
                (item['title'], item['pts'],
                 time.strftime('%Y-%m-%d', time.localtime(time.time()))))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class MusicPipeLine(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """
                insert into music_1(title, pts,`date`)value (%s,%s,%s)""",
                (item['title'], item['pts'],
                 time.strftime('%Y-%m-%d', time.localtime(time.time()))))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class Music7PipeLine(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """
                insert into music_7(title, pts,`date`)value (%s,%s,%s)""",
                (item['title'], item['pts'],
                 time.strftime('%Y-%m-%d', time.localtime(time.time()))))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class TagPipeLine(object):
    def __init__(self):
        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """insert into tag_data(tag_name,`datetime`)value (%s,%s)""",
                (item['tagName'], item['datetime']))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class TagPipeLine_2(object):
    def __init__(self):

        # 连接数据库
        self.connect = connect_db()
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 插入数据
            self.cursor.execute(
                """insert into tag_2(tag_name,`datetime`,`aid`)value (%s,%s,%s)""",
                (item['tagName'], item['datetime'], item['aid']))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class TagMongoPipeLine(object):
    def __init__(self):
        # 链接mongoDB
        self.client = MongoClient('localhost', 27017)

        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client['bili_data']  # 获得数据库的句柄
        self.coll = self.db['tag_data']  # 获得collection的句柄

    def process_item(self, item, spider):
        try:
            postItem = dict(item)  # 把item转化成字典形式
            self.coll.insert(postItem)  # 向数据库插入一条记录
            return item  # 会在控制台输出原item数据，可以选择不写
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item


class TagMongoPipeLine_2(object):
    def __init__(self):
        # 链接mongoDB
        self.client = MongoClient('localhost', 27017)

        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client['bili_data']  # 获得数据库的句柄
        self.coll = self.db['video']  # 获得collection的句柄

    def process_item(self, item, spider):
        try:
            postItem = dict(item)  # 把item转化成字典形式
            self.coll.update({
                "aid": int(item["aid"])
            }, {"$set": {
                'tag': postItem["tag"]
            }})
            return item  # 会在控制台输出原item数据，可以选择不写
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)


class TagMongoPipeLine_3(object):
    def __init__(self):
        # 链接mongoDB
        self.client = MongoClient('localhost', 27017)

        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client['bili_data']  # 获得数据库的句柄
        self.coll = self.db['video']  # 获得collection的句柄

    def process_item(self, item, spider):
        try:
            self.coll.update_one({
                "aid": int(item["aid"])
            }, {
                "$set": {
                    "author": item['author'],
                    "subChannel": item['subChannel'],
                    "channel": item['channel'],
                    "view": int(item['view']),
                    "favorite": int(item['favorite']),
                    "coin": int(item['coin']),
                    "share": int(item['share']),
                    "like": int(item['like']),
                    "dislike": int(item['dislike']),
                    "danmaku": int(item['danmaku']),
                    "title": item['title'],
                    "datetime": datetime.datetime.fromtimestamp(
                        item['datetime'])
                }
            }, True)
            return item
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)


class TagMongoPipeLine_4(object):
    def __init__(self):
        # 链接mongoDB
        self.client = MongoClient('localhost', 27017)

        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client['bili_data']  # 获得数据库的句柄
        self.coll = self.db['video2']  # 获得collection的句柄

    def process_item(self, item, spider):
        try:
            self.coll.insert({
                "aid":
                int(item["aid"]),
                "author":
                item['author'],
                "channel":
                item['channel'],
                "subChannel":
                item['subChannel'],
                "view":
                int(item['view']),
                "favorite":
                int(item['favorite']),
                "coin":
                int(item['coin']),
                "share":
                int(item['share']),
                "like":
                int(item['like']),
                "dislike":
                int(item['dislike']),
                "title":
                item['title'],
                "datetime":
                datetime.datetime.fromtimestamp(item['datetime'])
            })
            return item  # 会在控制台输出原item数据，可以选择不写
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)


# scrapy crawl tagSpider -s JOBDIR=tag-job -L INFO
class XiaoheiwuPipeline(object):
    def __init__(self):
        # 链接mongoDB
        self.client = MongoClient('localhost', 27017)
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client['bili_data']  # 获得数据库的句柄
        self.coll = self.db['xiaoheiwu']  # 获得collection的句柄

    def process_item(self, item, spider):
        try:
            self.coll.update_one({
                'id': item['pid']
            }, {
                '$set': {
                    'punishTitle': item['punishTitle'],
                    'punishTypeName': item['punishTypeName'],
                    'punishTime': item['punishTime'],
                    'reasonTypeName': item['reasonTypeName'],
                    'uid': item['uid'],
                    'originTypeName': item['originTypeName'],
                    'uname': item['uname'],
                    'blockedDays': item['blockedDays'],
                    'blockedType': item['blockedType'],
                    'originUrl': item['originUrl']
                }
            }, True)
            return item  # 会在控制台输出原item数据，可以选择不写
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)