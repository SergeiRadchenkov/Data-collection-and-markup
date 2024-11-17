import scrapy
from scrapy.http import HtmlResponse
from ..items import ImageItem


class UnsplashSpider(scrapy.Spider):
    name = 'unsplash'
    allowed_domains = ['unsplash.com']
    start_urls = ['https://unsplash.com/t/']

    def parse(self, response: HtmlResponse):
        category_links = response.xpath("//a[@class='_7wL9Z kXLw7']/@href").getall()
        for link in category_links:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response: HtmlResponse):
        category_name = response.xpath("//h1/text()").get().strip()

        image_count = 0
        max_images = 3  # Ограничение на количество фотографий

        image_links = response.xpath("//a[@itemprop='contentUrl']/@href").getall()
        for link in image_links:
            if image_count >= max_images:
                break 
            image_count += 1
            yield response.follow(link, callback=self.parse_image, meta={'category': category_name})

        # Отменил переход на следующую страницу, чтобы ограничить количество фото
        #next_page = response.xpath("//a[@rel='next']/@href").get() 
        #if next_page:
        #   yield response.follow(next_page, callback=self.parse_category)

    def parse_image(self, response: HtmlResponse):
        item = ImageItem()
        image_url = response.xpath("//meta[@property='og:image']/@content").get()
        item['image_urls'] = [image_url]
        item['image_title'] = response.xpath("//meta[@property='og:title']/@content").get()
        item['category'] = response.meta['category']
        yield item
