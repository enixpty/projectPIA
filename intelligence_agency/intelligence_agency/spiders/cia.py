from scrapy import Spider

class Cia(Spider):

    name = 'cia'
    start_urls = [
        'https://www.cia.gov/library/readingroom/historical-collections'
    ]
    custom_settings = {  
            "FEED_EXPORT" : 'utf-8',
            "ROBOTSTXT_OBEY" : True,
            "CONCURRENT_REQUEST" : 24,
            "MEMUSAGE_LIMIT_MB" : 2048,
            "MEMUSAGE_NOTIFY_MAIL" : ['munoz.melvin@gmail.com'],
            "USER_AGENT" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }

    def parse(self, response):
        urls=response.xpath('//a[starts-with(@href,"collection") and (parent::h3 or parent::h2)]/@href').getall()

        for link in urls :
            
            yield response.follow(link,callback=self.parse_link, cb_kwargs={'url' : response.urljoin(link)})

    
    def parse_link(self, response, **kwargs):
        
        link = kwargs['url'] 
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
        body  = response.xpath('//div[@class="field-item even"]/p[not(@class)]/text()').get() # solo se quiere el primer parrafo para referenciar

        yield {'title' : title,
                'body' : body,
                'url'  : link
            }