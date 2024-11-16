from scrapy.crawler import CrawlerProcess

from spiders.books import BooksSpider


if __name__ == "__main__":

    custom_settings = {
        'FEEDS': {
            'books.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True,
            },
        },
    }

    process = CrawlerProcess(settings=custom_settings)
    
    process.crawl(BooksSpider)
    process.start()