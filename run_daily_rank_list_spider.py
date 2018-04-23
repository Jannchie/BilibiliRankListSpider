import time

def crawl_work():
    command = 'scrapy crawl rankListDailySpider -o ' + './data/' + time.strftime("%Y-%m-%d") + '.json'
    os.system(command)

# run it every day
while True:
    time.sleep(86400)
    crawl_work()
        

