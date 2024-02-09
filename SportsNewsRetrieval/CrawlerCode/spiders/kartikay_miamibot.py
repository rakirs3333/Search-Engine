
import time
import datetime
import scrapy

class foxcrawler(scrapy.Spider):
    name = "flowRider"
    start_urls = []

    counter = 0
    
    def __init__(self):
        start = 1 #start page
        end = 66 #end page
        for i in range(start,end+1):
            self.start_urls.append(f'https://publicapi.misitemgr.com/webapi-public/v2/sections/5151/content?limit=1&offset={i}')
        super(foxcrawler, self).__init__() 

    def start_requests(self):
        for i in range(len(self.start_urls)):
            if (i+1) % 50 == 0:
                print("\nNOTE: Sleeping for 5 seconds after 50 requests.\n")
                time.sleep(5)
            
            yield scrapy.Request(url=self.start_urls[i], callback=self.parse)

    def parse(self, response):
        res = response.json()
        res = res['items'][0]
        #"https://www.miamiherald.com/sports" + str(
        url = res["url"].replace("https://www.mcclatchy-wires.com/incoming","")
        title = res["title"]
        time = datetime.datetime.fromtimestamp(res["published_date"]).strftime('%m/%d/%Y')
        text = res["summary"]
        yield {
            "title" : title,
            "time" : time,
            "url": url,
            "text": text  
        }

       