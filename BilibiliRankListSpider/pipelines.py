# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time

# import codecs


class BilibiliranklistspiderPipeline(object):

    def process_item(self, item, spider):
        t = time.strftime("%Y-%m-%d")
        with open(t + '.json', 'a') as f:
            json.dump(dict(item), f)
            f.write(',\n')
        return item