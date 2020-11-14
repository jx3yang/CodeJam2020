from product_crawlers.spiders.image import ImageSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from product_crawlers.settings import AMAZON_OUT_FILE, EBAY_OUT_FILE
import pandas as pd

if __name__ == '__main__':
    start_urls = list(pd.concat([
        pd.read_csv(AMAZON_OUT_FILE), pd.read_csv(EBAY_OUT_FILE)
    ])['image_url'])
    process = CrawlerProcess(get_project_settings())
    process.crawl(ImageSpider, start_urls=start_urls)
    process.start()
