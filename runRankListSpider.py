import time
import os

def crawl_work():
    command = 'scrapy crawl rankListSpider -o ' + './data/' + time.strftime("%Y-%m-%d") + '.json'
    os.system(command)

while True:
    time.sleep(86400)
    crawl_work()

        

