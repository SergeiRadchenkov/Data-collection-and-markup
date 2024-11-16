from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.hhru import HhruSpider



if __name__ == "__main__":

    custom_settings = {
        'FEEDS': {
            'hhru.json': {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 4,
                'overwrite': True,
            },
        },
    }

    process = CrawlerProcess(settings=custom_settings)
    
    process.crawl(HhruSpider)
    process.start()