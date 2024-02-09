import requests
import scrapy
import w3lib


class wta(scrapy.Spider):
    name = "wta"
    allowed_domains = ["wtatennis.com"]
    start_urls = ["https://www.wtatennis.com/news"]

    def parse(self, response):
        for i in range(1, 6):
            temp = f'//*[@id="main-content"]/section[2]/ul/li[{i}]/article/a/@href'
            x = response.xpath(temp).get()
            x='https://www.wtatennis.com'+x

            yield response.follow(url=x, callback=self.article,meta={'x':x})
        for j in range(1,4):
            urls = f'https://api.wtatennis.com/content/wta/text/en/?page={j}&pageSize=24&tagNames=News&references=&playlistTypeRestriction='
            headers = {'Content-Type': 'application/json'}
            for r in range(24):
                response = requests.get(url=urls)
                title = response.json()['content'][r]['title']
                body = response.json()['content'][r]['body']
                date=response.json()['content'][r]['date']
                id=str(response.json()['content'][r]['id'])
                tus=response.json()['content'][r]['titleUrlSegment']
                if (response.json()['content'][r]['titleUrlSegment']!=None):
                    url='https://www.wtatennis.com/news/'+id+'/'+tus
                else:
                    tus = title.replace(' ', '-')
                    tus = ''.join(e for e in tus if e.isalnum() or e == '-')
                    url = 'https://www.wtatennis.com/news/' + id + '/' + tus
                yield {
                    'title':title,
                    'date':date,
                    'url': url,
                    'news':(w3lib.html.remove_tags(body)).replace('\n',' ').replace('\r',' ')
                }

    def article(self, response):
        url=response.meta.get('x')
        title=response.xpath('//*[@id="main-content"]/article/header/div[2]/h1/text()').get().replace('\n',' ').replace('\t',' ').strip()
        date=(response.xpath('//*[@id="main-content"]/article/header/div[2]/div/time/text()').getall())[1].replace('\n',' ').replace('\t',' ').strip()
        news = response.xpath('//*[@id="main-content"]/article/div[1]/p/text()').getall()
        yield {
            'title':title,
            'date':date,
            'url':url,
            'news': news,
        }



