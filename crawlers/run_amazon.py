from product_crawlers.spiders.amazon import AmazonSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd

URLS_FILE = 'product_crawlers/amazon_urls.csv'

if __name__ == '__main__':
    start_urls = list(pd.read_csv(URLS_FILE)['url'])
    process = CrawlerProcess(get_project_settings())
    process.crawl(AmazonSpider, start_urls=start_urls)
    process.start()
