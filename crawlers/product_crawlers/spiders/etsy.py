import scrapy
from product_crawlers.items import ProductCrawlersItem
from product_crawlers.settings import ETSY_OUT_FILE

class EtsySpider(scrapy.Spider):
    name = 'etsy_spider'
    num_pages = 100

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': ETSY_OUT_FILE
    }

    def __init__(self, start_urls):
        self.start_urls = start_urls

    def set_page(self, url, page):
        return f'{url}?ref=pagination&page={page}'
    
    def start_requests(self):
        for url in self.start_urls:
            for page in range(1, self.num_pages+1):
                yield scrapy.Request(
                    url=self.set_page(url, page),
                    callback=self.parse_response
                )

    def parse_response(self, response):
        products = response.xpath('//ul[contains(@class, "responsive-listing-grid")]')[0].xpath('.//li[contains(@class, "wt-list-unstyled")]')
        for product in products:
            link_area = product.xpath('.//a[contains(@class, "listing-link")]')
            url = link_area.xpath('./@href').get()
            title = link_area.xpath('./@title').get()
            image_url = product.xpath('.//img[@data-listing-card-listing-image]/@src').get()

            text_area = product.xpath('.//div[contains(@class, "v2-listing-card__info")]')
            backup_title = text_area.xpath('.//h3/text()').get().strip()
            price = text_area.xpath('.//span[@class="currency-value"]/text()').get()
            yield ProductCrawlersItem(
                url=url,
                title=title,
                backup_title=backup_title,
                price=price,
                image_url=image_url
            )
