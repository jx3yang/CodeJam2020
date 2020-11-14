import scrapy
from product_crawlers.items import ProductCrawlersItem
from product_crawlers.settings import AMAZON_OUT_FILE

class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    num_pages = 50

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': AMAZON_OUT_FILE
    }

    def __init__(self, start_urls):
        self.start_urls = start_urls

    def set_page(self, url, page):
        return f'{url}&page={page}'
    
    def start_requests(self):
        for url in self.start_urls:
            for page in range(2, self.num_pages+2):
                yield scrapy.Request(
                    url=self.set_page(url, page),
                    callback=self.parse_response
                )

    def parse_response(self, response):
        products = response.xpath('//div[contains(@class, "s-main-slot")]')[0].xpath('.//div[@data-component-type="s-search-result"]')
        for product in products:
            title_area = product.xpath('.//h2/a[contains(@class, "a-link-normal")]')[0]
            url = title_area.xpath('./@href').get()
            title = title_area.xpath('./span/text()').get()
            price = product.xpath('.//span[@class="a-price"]//text()').get()
            image_url = product.xpath('.//img[@class="s-image"]/@src').get()
            backup_title = product.xpath('.//img[@class="s-image"]/@alt').get()
            yield ProductCrawlersItem(
                url=url,
                title=title,
                backup_title=backup_title,
                price=price,
                image_url=image_url
            )
