# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time
import pymysql
import configparser

# 自己创建的database配置文件，其中包含数据库链接信息。
import logging


# 单位换算，化为K（千）。
def unit_convert(item):
    if item['barrage'][-1] == u'万':
        item['barrage'] = float(item['barrage'][:-1]) * 10
    else:
        item['barrage'] = float(item['barrage']) / 1000
    if item['play'][-1] == u'万':
        item['play'] = float(item['play'][:-1]) * 10
    else:
        item['play'] = float(item['play']) / 1000


def connect_db():

    cf = configparser.ConfigParser()
    cf.read("db.conf")
    connect = pymysql.connect(
        host=cf.get('MYSQL', 'HOST'),
        db=cf.get('MYSQL', 'DBNAME'),
        user=cf.get('MYSQL', 'USER'),
        passwd=cf.get('MYSQL', 'PASSWD'),
        charset='utf8',
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
                (item['title'], item['author'], item['barrage'], item['play'],
                 item['pts'], item['href'], item['partition'],
                 item['subPartition'], item['fans'], item['submissions']))
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
                (item['title'], item['author'], item['barrage'], item['play'],
                 item['pts'], item['href'], item['partition'],
                 item['subPartition'], item['fans'], item['submissions']))
            # 提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误日志
            logging.error(error)
        return item