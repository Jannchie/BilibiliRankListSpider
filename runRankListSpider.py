
import schedule
import time
import subprocess
import logging

def crawl_work():
    command = 'scrapy crawl rankListSpider -o ' + './data/' + time.strftime("%Y-%m-%d") + '.json'
    logging.info(command)
    subprocess.Popen(command,shell=True) # Execute a child program in a new process.


# run it every day
logging.info('rankListSpider running!Crawling once a day..')
schedule.every(1).days.do(crawl_work)

while True:
    schedule.run_pending()

        

