import scrapy


class ProductCrawlersItem(scrapy.Item):
    url = scrapy.Field()
    image_url = scrapy.Field()
    title = scrapy.Field()
    backup_title = scrapy.Field()
    price = scrapy.Field()

class ImageHashItem(scrapy.Item):
    url = scrapy.Field()
    image_hash = scrapy.Field()
