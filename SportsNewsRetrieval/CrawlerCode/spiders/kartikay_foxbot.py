import time
import json
import scrapy

class foxcrawler(scrapy.Spider):
    name = "foxbot"
    allowed_domains = ["foxnews.com"]
    start_urls = []

    counter = 0
    
    def __init__(self):
        start = 1 #start page
        end = 9900 #end page
        for i in range(start,end+1):
            self.start_urls.append(f'https://www.foxnews.com/api/article-search?searchBy=tags&values=fox-news%2Fsports%2Fnfl&excludeBy=tags&excludeValues=&size=1&from={i}&isSection=true')
        super(foxcrawler, self).__init__() 

    def start_requests(self):
        for i in range(len(self.start_urls)):
            if (i+1) % 50 == 0:
                print("\nNOTE: Sleeping for 5 seconds after 50 requests.\n")
                time.sleep(5)
            
            yield scrapy.Request(url=self.start_urls[i], callback=self.parse)

    def parse(self, response):
        res = response.json()
        res = res[0]
        title = res['title']
        url = res["url"]
        if "video" not in url:
            url = "https://www.foxnews.com" + url
        
        text = res["description"]
        time = res["publicationDate"]
        
        yield {
            "title" : title,
            "time" : time,
            "url": url,
            "text": text  
        }

       