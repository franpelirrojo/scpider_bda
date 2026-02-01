import scrapy
from scrapy.crawler import CrawlerProcess

class NoticiasSpider(scrapy.Spider):
    name = "NoticiasSpider"

    def __init__(self, config, *args, **kwargs):
        super(NoticiasSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = config.get("allowed_domains")
        self.start_urls = config.get("start_urls")
        self.noticias_link = config.get("noticias_link")
        self.fields = config.get("fields")

    def parse(self, response):
        noticias = response.css(self.noticias_link).getall()
        yield from response.follow_all(noticias, callback=self.parse_noticia)

    def parse_noticia(self, response):
        item = {}
        for field, selector in self.fields.items():
            item[field] = response.css(selector).get()
            if isinstance(item[field], str): 
                item[field] =  item[field].strip("\n\" ")

        item["source"] = response.url
        yield item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        if "feeds" in kwargs:
            spider.settings.set(
                "FEEDS", {kwargs['feeds'] : {'format': 'csv', 'overwrite': True}}, priority="spider")
        return spider


def run(periodicos):
    settings = {
        "USER_AGENT": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36",
        "LOG_LEVEL": "DEBUG",
        "CONCURRENT_REQUESTS" : 100,
        "CONCURRENT_REQUESTS_PER_DOMAIN" : 100,
        "DOWNLOAD_DELAY" : 3,
        "DOWNLOAD_TIMEOUT" : 10,
        "COOKIES_ENABLED" : False
    }

    process = CrawlerProcess(settings)

    for config in periodicos:
        process.crawl(NoticiasSpider, config=config, feeds=config['output_file'])

    process.start()

if __name__ == "__main__":
    periodicos = [
        {
            "allowed_domains": ["www.eldiario.es", "eldiario.es"],
            "start_urls": ["https://www.eldiario.es/"],
            "output_file": "eldiario.csv",
            "noticias_link": "h2>a::attr(href)",
            "fields": {
                "title": "h1.title::text",
                "description": "ul.footer h2::text",
                "autor": "p.authors>a::text",
                "date": "div.date>span.day::text",
                "hour": "div.date>span.hour::text"
            }
        },
        {
            "allowed_domains": ["elpais.com", "www.elpais.com", "cincodisas.es"],
            "start_urls": ["https://elpais.com/"],
            "output_file": "elpais.csv",
            "noticias_link": "article *.c_t>a::attr(href)",
            "fields": {
                "title": "h1.a_t::text",
                "description": "p.a_st::text",
                "autor": "div[data-dtm-region=articulo_firma] > a::text",
                "date": "a[data-date]::attr(data-date)"
            }
        },
        {
            "allowed_domains": ["diariosocialista.net"],
            "start_urls": ["https://diariosocialista.net/"],
            "output_file": "ds.csv",
            "noticias_link": "*.cover-widget-item-title>a::attr(href)",
            "fields": {
                "title": "h1.post-title::text",
                "description": "div.post-excerpt>p::text",
                "date": "div.post-meta-date::text"
            }
        }
    ]

    run(periodicos)
