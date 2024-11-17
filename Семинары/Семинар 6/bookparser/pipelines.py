# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import json
import scrapy


class BookparserPipeline:
    def __init__(self):
        self.file = open('books.json', 'w', encoding='utf-8')
        self.file.write('[\n') 
        self.first_item = True

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')  
        json.dump(dict(item), self.file, ensure_ascii=False, indent=4)
        self.first_item = False
        return item

    def close_spider(self, spider):
        self.file.write('\n]') 
        self.file.close()


class BookPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img_url in item['photos']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)
        # return super().get_media_requests(item, info)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if item[0]]
        return item