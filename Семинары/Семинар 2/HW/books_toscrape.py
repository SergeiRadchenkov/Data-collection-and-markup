'''
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ 
и извлечь информацию о всех книгах на сайте во всех категориях: 
название, 
цену, 
количество товара в наличии (In stock (19 available)) в формате integer, 
описание.

Затем сохранить эту информацию в JSON-файле.'''
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

ua = UserAgent()

url = 'https://books.toscrape.com/catalogue/'
headers = {'User-Agent': ua.random}
page = 1

session = requests.session()

all_books = []

while True:
    response = session.get(url + f'page-{page}.html', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', {'class': 'product_pod'})
    if not books:
        break

    for book in books:
        book_info = {}

        title_info = book.find('h3')
        book_info['title'] = title_info.getText()

        price_info = book.find('p', {'class': 'price_color'})
        book_info['price'] = float(price_info.getText().replace('Â£', ''))

        url_book = url + book.find('a').get('href')

        response_link = requests.get(url_book)
        soup_link = BeautifulSoup(response_link.text, 'html.parser')
        book_link_blocks = soup_link.find_all('article', {'class': 'product_page'})

        for block in book_link_blocks:
            stock_info = block.find('p', {'class': 'instock availability'})
            book_info['stock'] = int(stock_info.getText().replace('\n\n    \n        In stock (', '').replace(' available)\n    \n', ''))

            book_info_temp = block.find_all('p')
            for text in book_info_temp:
                if len(text.getText()) > 50:
                    book_info['description'] = text.getText()

        all_books.append(book_info)
    print(f'Обработана {page} страница')
    page += 1

with open('books.toscrape.json', 'w') as f:
    json.dump(all_books, f)