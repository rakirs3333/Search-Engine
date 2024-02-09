import scrapy
import w3lib


class mls(scrapy.Spider):
    name = "mls"
    allowed_domains = ["mlssoccer.com"]
    start_urls = ["https://www.mlssoccer.com/news/"]

    def parse(self, response):
        for i in range(1,500):
            path=('https://www.mlssoccer.com/news/'+f'more/{i}')
            if(i>32):
                yield response.follow(path, callback=self.news,meta={'url':path})

    def news(self,response):
        url = response.meta.get('url')
        for i in range(2,33):
            page=response.xpath(f'//*[@id="main-content"]/section[2]/div/div[1]/section/div[2]/div[{i}]/a/@href').get()
            page="https://www.mlssoccer.com"+page
            yield response.follow(page,callback=self.article,meta={'url':page})

    def article(self,response):
        url = response.meta.get('url')
        date = response.xpath('//*[@id="main-content"]/section[1]/div/div/article/div[1]/div[2]/div[3]/p').get()
        if(date==None):
            date=response.xpath('// *[ @ id = "main-content"] / section[1] / div / div / article / div[1] / div / div[3] / p').get()
        title=response.xpath('//*[@id="main-content"]/section[1]/div/div/article/div[1]/h1/text()').get().replace('\n',' ').strip()
        news=response.xpath('//*[@id="main-content"]/section[1]/div/div/article/div[3]/div/div[1]').get()
        news=(w3lib.html.remove_tags(news)).replace('\n','').strip()


        yield {
            'title': title,
            'date': date,
            'url': url,
            'text': news,
        }
