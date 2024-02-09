import time
import scrapy

class nbacrawler(scrapy.Spider):
    name = "nbabot"
    allowed_domains = ["nba.com"]
    start_urls = []

    counter = 0
    
    def __init__(self):
        start = 1 #start page
        end = 1610 #end page
        for i in range(start,end+1):
            self.start_urls.append(f'https://content-api-prod.nba.com/public/1/leagues/nba/content?page={i}&count=12&types=post&exclude-id=1034176%2C1027831%2C1025281%2C1030018%2C1032638%2C1033171%2C1032440%2C1032402%2C1032407%2C996608%2C1030856%2C1032072%2C1032125%2C1031392%2C1031574%2C1031140%2C1031630%2C1031121%2C1031387&region=united-states')
        super(nbacrawler, self).__init__() 
    # def start_requests(self):

    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    
    def start_requests(self):
        
        for i in range(len(self.start_urls)):
            if i % 50 == 0:
                print("\nNOTE: Sleeping for 15 seconds after 50 requests.\n")
                time.sleep(15)
            yield scrapy.Request(url=self.start_urls[i], callback=self.parse)

    def parse(self, response):
        res = response.json()
        items = res['results']['items']

        for item in items:
            title = item['title']
            url = item["permalink"]
            text = item["excerpt"]
            time = item["date"]
            #print(title, url, text)
            yield {
                "title" : title,
                "time" : time,
                "url": url,
                "text": text  
            }

        
        # for i in range(1,1610):
        #     if i % 50 == 0:
        #         print("\nNOTE: Sleeping for 15 seconds before crawling.\n")
        #         time.sleep(15)
        #     top_url = f'https://content-api-prod.nba.com/public/1/leagues/nba/content?page={i}&count=12&types=post&exclude-id=1034176%2C1027831%2C1025281%2C1030018%2C1032638%2C1033171%2C1032440%2C1032402%2C1032407%2C996608%2C1030856%2C1032072%2C1032125%2C1031392%2C1031574%2C1031140%2C1031630%2C1031121%2C1031387&region=united-states'
        #     yield response.follow(top_url, callback=self.nextpage)


    # def nextpage(self, response):
    #     res = response.json()
    #     items = res['results']['items']

    #     for item in items:
    #         title = item['title']
    #         url = item["permalink"]
    #         text = item["excerpt"]
    #         time = item["date"]
    #         #print(title, url, text)
    #         yield {
    #             "title" : title,
    #             "time" : time,
    #             "url": url,
    #             "text": text  
    #         }