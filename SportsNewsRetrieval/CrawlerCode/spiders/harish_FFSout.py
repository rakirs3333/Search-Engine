import scrapy

class FFScoutNews(scrapy.Spider):
    name = "ffscout"
    allowed_domains = []
    start_urls = ["https://www.fantasyfootballscout.co.uk/articles/"]


    def nextpage(self, response):
        print('nextPage')
        title = response.css('h1.entry-title::text').get()
        divs = response.css('div.article-holder')
        paras = ''
        for para in divs.css('p::text').getall(): 
            paras = paras + '\n' + para
        yield{
                'title':title,
                'text':paras,
                'url':response.request.meta['url']
            }
    
    def parse(self, response):
        print('parse')
        linkstemp = response.css('div.inside.articles')
        links = linkstemp.css('article')
        seen = set()
        for link in links:
            if link not in seen:
                seen.add(link)
                each_link = link.css('a').attrib['href']
                print("parse"+each_link)
                yield response.follow(each_link, callback=self.nextpage, meta={'url': each_link})
        next_page = response.css('a.ffs_btn').attrib['href']
        yield response.follow(next_page,callback=self.parse)