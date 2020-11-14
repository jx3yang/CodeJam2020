from product_crawlers.spiders.ebay import EbaySpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd

URLS_FILE = 'product_crawlers/ebay_urls.csv'

if __name__ == '__main__':
    start_urls = list(pd.read_csv(URLS_FILE)['url'])
    process = CrawlerProcess(get_project_settings())
    process.crawl(EbaySpider, start_urls=start_urls)
    process.start()
