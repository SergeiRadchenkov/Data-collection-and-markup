import scrapy
from scrapy.http import HtmlResponse
from items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=python&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"]


    def parse(self, response: HtmlResponse):

        next_page = response.xpath('//a[@data-qa="number-pages-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//span[@data-qa="serp-item__title-text"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1[@data-qa="vacancy-title"]/text()').get()
        salary = response.xpath('//span[@data-qa="vacancy-salary-compensation-type-gross"]//text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
