import scrapy
import json


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=python&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"]

    def parse(self, response):
        links = response.css('//a[@data-qa="serp-item__title"]/@href').getall()
        for link in links:
            data = {
                'name': link.css('//h1[@data-qa="vacancy-title"]/span/text()').get(),
                'salary': link.css('//span[@data-qa="vacancy-salary-compensation-type-gross"]/text()').getall(),
                'url': link.url
            }

            self.save_to_json(data)
            yield data

        next_page = response.css('//a[@data-qa="number-pages-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)


        
    def save_to_json(self, data):
        with open('hhru.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.write(",\n")

