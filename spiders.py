#!/usr/bin/python3
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response

class GadgetSpider(Spider):
    def __init__(self, start_urls, queue=None, *args, **kwargs):
        self.start_urls = start_urls
        if queue is not None:
            self.queue = queue
        super(GadgetSpider, self).__init__(*args, **kwargs)


class GsmArenaBrandsSpider(GadgetSpider):
    name = 'www.gsmarena.com'
    start_urls = ['http://www.gsmarena.com/makers.php3']

    def parse(self, response):
        relative_brand_urls = response.xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]/a/@href').extract()
        absolute_brand_urls = []
        for url in relative_brand_urls:
            absolute_url = 'http://www.gsmarena.com/' + url
            absolute_brand_urls.append(absolute_url)
        GsmArenaBrandSpider.start_urls.extend(absolute_brand_urls)

class GsmArenaBrandSpider(GadgetSpider):
    name = 'com.gsmarena.www.brands'
    start_urls = []

    def parse(self, response):
        relative_brand_urls = response.xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/ul/li[1]/a').extract()
        absolute_brand_urls = []
        for url in relative_brand_urls:
            absolute_url = 'http://www.gsmarena.com/' + url
            absolute_brand_urls.append(absolute_url)
        GsmArenaPhoneSpider.start_urls.extend(absolute_brand_urls)

class GsmArenaPhoneSpider(Spider):
    name = 'com.gsmarena.www.phones'
    start_urls = []

    def parse(self, response):


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(GsmArenaBrandsSpider)
process.crawl(GsmArenaBrandsSpider)
process.crawl(GsmArenaPhoneSpider)

#class GSMArenaCrawlerQueue(object):
#    def __init__(self):
#        super(GSMArenaCrawlerStack, self).__init__()
#        self.crawlers = []
#
#    def next_spider(self):
#        if self.crawlers is not None and len(self.crawlers) is not 0:
#            while len(self.crawlers) > 0:
#                spider_class, urls = self.crawlers.pop()
#                spider = spider_class
#                spider.start_urls = urls

