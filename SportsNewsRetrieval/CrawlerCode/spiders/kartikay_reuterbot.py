from pathlib import Path
import time
import scrapy

class reutercrawler(scrapy.Spider):
    name = "reutbot"
    allowed_domains = ["reuters.com"]
    start_urls = []
    

    def __init__(self):
        start = 1 #start page
        end = 3277 #end page
        for i in range(start,end+1):
            self.start_urls.append(f'https://www.reuters.com/news/archive/sportsNews?view=page&page={i}&pageSize=10')
        super(reutercrawler, self).__init__() 
        
    # 3277 yaad rakhna

    def start_requests(self):
        
        for i in range(len(self.start_urls)):
            if i % 50 == 0:
                print("\nNOTE: Sleeping for 15 seconds after 50 requests.\n")
                time.sleep(15)
            yield scrapy.Request(url=self.start_urls[i], callback=self.parse)


    def parse(self, response):
        for i in range(1,10):
            titlex = f'//*[@id="content"]/section[2]/div/div[1]/section/section/div/article[{i}]/div[2]/a/h3/text()'
            textx = f'//*[@id="content"]/section[2]/div/div[1]/section/section/div/article[{i}]/div[2]/p/text()'
            urlx = f'//*[@id="content"]/section[2]/div/div[1]/section/section/div/article[{i}]/div[2]/a/@href'
            timex = f'//*[@id="content"]/section[2]/div/div[1]/section/section/div/article[{i}]/div[2]/time/span/text()'

            title = response.xpath(titlex).get().strip()
            url = 'reuters.com' + response.xpath(urlx).get().strip()
            text = response.xpath(textx).get().strip()
            time = response.xpath(timex).get().strip()

            yield {
                "title": title,
                "time": time,
                "url": url,
                "text": text
            }
