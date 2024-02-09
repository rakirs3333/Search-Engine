import scrapy
import pandas as pd
from scrapy.http.request import Request
# from postscrape.items import PostscrapeItem
from scrapy.loader.processors import MapCompose, Join

from scrapy.loader import ItemLoader
import re
class PostsSpider(scrapy.Spider):
    name = "posts"
    
    start_urls = [
        

        'https://www.futhead.com/10/players/',
       
        ]

    def parse(self,response):
        names = []
   
        post =response.css('.col-flex-300')
        o=0
        
        count = response.css('.pagination span::text').get().replace("\n","").replace(" ","").replace("of156","")
        
        curr_page = 'https://www.futhead.com/10/players/?page='+str(count)
        for p in post.css('.player-info'):
            x = post.css('.player-info')[o]
            name = x.css('.player-name::text').get()
            player_details = x.css('.player-club-league-name::text').getall()
            yield{
                'title' : name,
                'text' : player_details,
                'url': curr_page 
            }
            o=o+1
        print (response.request.url)
    
        page_no = int(count) + 1
        
        next_page = 'https://www.futhead.com/10/players/?page='+str(page_no)
        print (next_page)

        if (next_page is not None) :
            yield response.follow(next_page,callback = self.parse)
    



