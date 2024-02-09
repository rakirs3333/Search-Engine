import scrapy
import w3lib


class nfl(scrapy.Spider):
    name = "nfl"
    allowed_domains = ["cbssports.com"]
    start_urls = ["https://www.cbssports.com/nfl"]

    def parse(self, response):
        for i in range(1,601):
            path=('https://www.cbssports.com/nfl'+f'/{i}')
            yield response.follow(path, callback=self.news,meta={'url':path})

    def news(self,response):
        url = response.meta.get('url')

        for i in range(1,11):
            for j in range(1,4):
                pages = response.xpath(f'// *[ @ id = "page-content"] / div[2] / div / div[3] / div / ul / div / ul[{i}]/ li[{j}]/ h5 / a / @ href').get()
                page="https://www.cbssports.com"+pages
                yield response.follow(page,callback=self.article,meta={'url':page})

    def article(self,response):
        url = response.meta.get('url')
        date=response.xpath('//*[@id="article0"]/article/div[3]/div[2]/div/div[2]/time/text()').get().replace('\n',' ').strip()
        title=response.xpath('//*[@id="article0"]/article/div[3]/h1/text()').get().replace('\n',' ').strip()
        news=response.xpath('//*[@id="Article-body"]/div[2]').get().replace('\t',' ').strip()
        news=(w3lib.html.remove_tags(news)).replace('\n','').strip()


        yield {
            'title': title,
            'date': date,
            'url': url,
            'text': news,
        }
