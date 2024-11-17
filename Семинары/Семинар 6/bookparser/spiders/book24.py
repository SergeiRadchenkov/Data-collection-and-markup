import scrapy
from scrapy.http import HtmlResponse
from items import BookparserItem
from scrapy.loader import ItemLoader


class Book24Spider(scrapy.Spider):
    name = "book24"
    allowed_domains = ["book24.ru"]
    # start_urls = ["https://book24.ru/search/?q=фантастика"]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://book24.ru/catalog/fantastika-1649/']


    def parse(self, response: HtmlResponse):
        links = response.xpath('//article[@class="product-card"]').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_book)
        
    
    def parse_book(self, response: HtmlResponse):

        loader = ItemLoader(item=BookparserItem(), response=response)
        loader.add_xpath('name', "//h1[@class='product-detail-page__title']/text()")
        loader.add_xpath('price', "//span[@class='app-price product-sidebar-price__price']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', "//div[@class='product-poster__main-slide']/picture/img[@class='product-poster__main-image']/@src")

        yield loader.load_item()