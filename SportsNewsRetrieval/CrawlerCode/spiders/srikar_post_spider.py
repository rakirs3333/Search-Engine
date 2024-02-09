import scrapy   #importing scrapy

class ESPNSpider(scrapy.Spider): #this is our spider class 
    name= "posting" #this is the name for the file which we will use instead of the file name while crawling.
    list=['january','february','march','april','may','june','july','august','september','october','november','december']
    start_urls=[            #this is the list of all the websites to crawl
        f'https://www.espn.com/nfl/news/archive/_/month/{months}' for months in list
        #f'http://www.espn.com/nba/news/archive/_/month/{months}' for months in list
        #f'http://www.espn.com/mlb/news/archive/_/month/{months}' for months in list
    ]
    def otherpage(self,response): #
        links_list = response.css('ul.inline-list li')
        for link in links_list:
            every_link = link.css('a').attrib['href']
            yield response.follow(every_link, callback=self.nextpage, meta={'url': every_link})
        self.parse()
    def nextpage(self,response):  #this is the method to crawl data from the next page followed from the link
        title=response.css('header.article-header h1::text').get()
        #divs = response.css('div.c-text')
        info=''
        for para in response.css('p::text').getall(): 
            info = info + '\n' + para
        if title and info :
            yield{
            'title':title,
            'text':info,
            'url':response.request.meta['url']
            }
    def parse(self, response):              # this method is used to define how crawling is done ul.inline-list li
        links_list = response.css('div.article a')
        for link in links_list:
            every_link = link.css('a').attrib['href']
            yield response.follow(every_link, callback=self.otherpage, meta={'url': every_link})  #this is used to get into each link with the attribute and crawl the data on that page
      