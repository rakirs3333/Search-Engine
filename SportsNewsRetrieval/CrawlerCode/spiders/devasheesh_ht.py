import scrapy


class ht(scrapy.Spider):
    name = "ht"
    allowed_domains = ["hindustantimes.com"]
    start_urls = ["https://www.hindustantimes.com/sports"]

    def parse(self, response):
        for i in range(1,52):
            path=('https://www.hindustantimes.com/sports'+f'/others/page-{i}')
            yield response.follow(path, callback=self.news,meta={'url':path})

    def news(self,response):
        url = response.meta.get('url')
        for i in range(2,42):
            page=response.xpath(f'//*[@id="dataHolder"]/div[{i}]/h3/a/@href').get()
            page="https://www.hindustantimes.com"+page
            yield response.follow(page,callback=self.article,meta={'url':page})

    def article(self,response):
        url = response.meta.get('url')
        title=response.xpath('//*[@id="dataHolder"]/div[1]/h1/text()').get()
        news=response.xpath('// *[ @ id = "dataHolder"] / div[1] / div[4] / div[1]/p/text()').getall()
        date=response.xpath('//*[@id="dataHolder"]/div[1]/div[1]/div[2]/text()').get()

        yield {
            'title': title,
            'date': date,
            'url': url,
            'text': news,
        }
