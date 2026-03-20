# Scrapy settings for jobs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jobs'

SPIDER_MODULES = ['jobs.spiders']
NEWSPIDER_MODULE = 'jobs.spiders'

# Obey robots.txt rules - CRITICAL for ethical scraping
ROBOTSTXT_OBEY = True

# Set proper User-Agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Configure pipelines
ITEM_PIPELINES = {
    'jobs.pipelines.JobsPipeline': 300,
}

# Download timeout
DOWNLOAD_TIMEOUT = 30

# Crawl rate limiting - POLITE SCRAPING
DOWNLOAD_DELAY = 2  # 2-second delay between requests

# AutoThrottle extension for adaptive delays
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Request/Response settings
CONCURRENT_REQUESTS = 1  # One request at a time for polite behavior
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = 'httpcache'

# Logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# Retry settings
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]