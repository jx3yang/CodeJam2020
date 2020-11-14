BOT_NAME = 'product_crawlers'

SPIDER_MODULES = ['product_crawlers.spiders']
NEWSPIDER_MODULE = 'product_crawlers.spiders'

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 1

AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

RETRY_TIMES = 10
RETRY_HTTP_CODES = [301]

AMAZON_OUT_FILE = 'output/amazon.csv'
EBAY_OUT_FILE = 'output/ebay.csv'
IMAGE_HASH_FILE = 'output/image_hash.csv'
