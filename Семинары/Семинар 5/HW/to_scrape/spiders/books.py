import scrapy
import json


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            data = {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('div.product_price p.price_color::text').get(),
                'availability': book.css('div.product_price p.instock.availability::text').re_first(r'\S+'),
                'rating': book.css('p.star-rating::attr(class)').re_first(r'star-rating (\w+)'),
            }

            self.save_to_json(data)
            yield data

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

        
    def save_to_json(self, data):
        with open('books.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.write(",\n")
