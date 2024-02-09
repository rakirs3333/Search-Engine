import time
import scrapy


# for this website setting robots.txt True
# fair use

class tenniscrawl(scrapy.Spider):
    name = "ennis"
    start_urls = []

    
    def __init__(self):
        start = 1 #start page
        end = 356 #end page
        for i in range(start,end+1):
            self.start_urls.append(f'https://caasports.com/services/archives.ashx/stories?index={i}&page_size=1&sport=tennis&school=0&season=0&search=')
        super(tenniscrawl, self).__init__() 

    def start_requests(self):
        for i in range(len(self.start_urls)):
            if (i+1) % 50 == 0:
                print("\nNOTE: Sleeping for 5 seconds after 50 requests.\n")
                time.sleep(5)
            
            yield scrapy.Request(url=self.start_urls[i], callback=self.parse)

    def parse(self, response):
        res = response.json()
        res = res['data'][0]

        url = "caasports.com"+res["story_path"]
        title = res["story_headline"]
        time = res["story_postdate"]
        text = res["story_summary"]
        yield {
            "title" : title,
            "time" : time,
            "url": url,
            "text": text  
        }

       