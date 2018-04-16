from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
import scrapy


class CustomProcess(CrawlerProcess):
    def __init__(self, *a, **kw):
        super(CustomProcess, self).__init__(*a, **kw)

    def create_crawler(self, spider_class, *a, **kw):
        crawler = super(CustomProcess, self).create_crawler(spider_class)
        if kw is not None:
            for k, v in kw.items():
                if k is "callback":
                    crawler.finish_callback = v

        return crawler

    def crawl(self, spider_class, *a, **kw):
        cb = None
        if kw is not None:
            for k, v in kw.items():
                if k is "callback":
                    cb = v
        crawler = self.create_crawler(spider_class, callback=cb)
        return self._crawl(crawler, *a, **kw)


class SpiderCoordinator:
    def __init__(self, settings={}, process=None):
        if not process:
            if len(settings.keys()) > 0:
                process = self._new_process(settings)
        self.process = process
        self.settings = process.settings
        self.results = None

    def add_spider(self, spider, callback=None):
        self.process.crawl(spider, callback=callback)


    def add_spiders(self, spider_list, callback=None):
        for spider in spider_list:
            self.add_spider(spider, callback)

    def _new_process(self, settings=None):
        if not settings:
            return CustomProcess(self.settings)
        return CustomProcess(settings)

    def start(self):
        self.process.start()
        return self.results
    
    def process_results(self, results):
        spiders = []
        for name, url in results.items():
            spiders.append(define_custom_spider(name, url))
        self.results = spiders



class EnumSpider(Spider):
    def __init__(self, *a, **kw):
        super(EnumSpider, self).__init__(*a, **kw)


class BrandEnumSpider(EnumSpider):
    name = 'www.gsmarena.com/brands'
    start_urls = ['http://www.gsmarena.com/makers.php3']
    start_urls = ['https://webcache.googleusercontent.com/search?q=cache:u8gj9AaWq-MJ:https://www.gsmarena.com/makers.php3+&cd=1&hl=en&ct=clnk&gl=pe']
    start_urls = ['http://web.archive.org/web/20180415144451/https://www.gsmarena.com/makers.php3']

    def __init__(self, *a, **kw):
        super(BrandEnumSpider, self).__init__(*a, **kw)

    def parse(self, response):
        brand_names = response.xpath('//html/body/div/div/div/div/div/table/tr/td/a/text()').getall()
        brands_urls = response.xpath('//html/body/div/div/div/div/div/table/tr/td/a/@href').getall()
        results = {}
        for index in range(0, len(brand_names)):
            results[brand_names[index]] = brands_urls[index]

        if self.callback:
            self.callback(results)
        return results


class BrandSpider(EnumSpider):
    def __init__(self, *a, **kw):
        super(BrandSpider, self).__init__(*a, **kw)

    def parse(self, response):
        devices_names = response.xpath('//html/body/div/#wrapper/#outer/#body/div/#review-body/div/ul/li/a/@href').getall()
        devices_url = response.xpath('//html/body/div/#wrapper/#outer/#body/div/#review-body/div/ul/li/a/@href').getall()
        return


def define_custom_spider(spider_name, spider_url):
    name = spider_name.strip(" ")
    class NewBrandSpider(BrandSpider):
        name = spider_name.strip("")
        start_urls = [spider_url]

        def __init__(self, *a, **kw):
            super(NewBrandSpider, self).__init__(*a, **kw)

        def parse(self, response):
            import pudb;pudb.set_trace()
            return

    NewBrandSpider.__qualname__ = name + 'Spider'

    return NewBrandSpider

def echo(jsonstring, filename="results.json"):
    with open('rw', filename) as file:
        file.write(jsonstring)


def main():
    settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    }
    process = CustomProcess(settings)

    coordinator = SpiderCoordinator(settings, process)
    coordinator.add_spider(BrandEnumSpider, coordinator.process_results)
    spiders = coordinator.start()
    coordinator = SpiderCoordinator(settings, process)
    coordinator.add_spiders(spiders, echo)

if __name__ == "__main__":
    main()
