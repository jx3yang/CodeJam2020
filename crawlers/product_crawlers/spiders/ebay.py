import scrapy
from product_crawlers.items import ProductCrawlersItem
from product_crawlers.settings import EBAY_OUT_FILE

class EbaySpider(scrapy.Spider):
    name = 'ebay_spider'
    num_pages = 4

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': EBAY_OUT_FILE
    }

    def __init__(self, start_urls):
        self.start_urls = start_urls

    def set_page(self, url, page):
        return f'{url}?_pgn={page}'
    
    def start_requests(self):
        for url in self.start_urls:
            for page in range(1, self.num_pages+1):
                yield scrapy.Request(
                    url=self.set_page(url, page),
                    callback=self.parse_response
                )

    def parse_response(self, response):
        products = response.xpath('//ul[contains(@class, "b-list__items_nofooter")]//li')
        for product in products:
            info_area = product.xpath('.//div[contains(@class, "s-item__info")]')
            price = info_area.xpath('.//span[@class="s-item__price"]/text()').get()
            title_area = info_area.xpath('.//a[@class="s-item__link"]')
            url = title_area.xpath('./@href').get()
            title = title_area.xpath('.//text()').get()
            image_url = product.xpath('.//img[@class="s-item__image-img"]/@src').get()
            backup_title = product.xpath('.//img[@class="s-item__image-img"]/@alt').get()
            yield ProductCrawlersItem(
                url=url,
                title=title,
                backup_title=backup_title,
                price=price,
                image_url=image_url
            )
