
import schedule
import time
import subprocess

def crawl_work():
    subprocess.Popen('scrapy crawl rankListSpider -o '+ './data/' + time.strftime("%Y-%m-%d") + '.json') # Execute a child program in a new process.


# run it every day
schedule.every(1).days.do(crawl_work)
while True:
    schedule.run_pending()

        