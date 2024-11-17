# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class UnsplashScraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveToCsvPipeline:
    def open_spider(self, spider):
        self.file = open('images_data.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Category', 'Title', 'URL'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        image_path = item.get('image_paths', [None])[0] 
        self.writer.writerow([
            item['category'],
            item['image_title'],
            item['image_urls'],
            #image_path,
        ])
        return item