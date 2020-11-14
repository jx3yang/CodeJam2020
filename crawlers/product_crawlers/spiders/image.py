import scrapy
from product_crawlers.items import ImageHashItem
from product_crawlers.settings import IMAGE_HASH_FILE
from PIL import Image
from io import BytesIO
import imagehash

class ImageSpider(scrapy.Spider):
    name = 'image_spider'

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': IMAGE_HASH_FILE
    }

    def __init__(self, start_urls):
        self.start_urls = start_urls

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
    
    def parse(self, response):
        yield ImageHashItem(
            url=response.request.url,
            image_hash=list(imagehash.phash(Image.open(BytesIO(response.body))).hash.astype(int).flatten())
        )
