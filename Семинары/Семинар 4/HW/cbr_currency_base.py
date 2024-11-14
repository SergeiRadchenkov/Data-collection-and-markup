from lxml import html
import requests
import csv


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36'}

url = 'https://cbr.ru/currency_base/daily'

response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

currencies = []
currency_list = {}
items = dom.xpath('////table[@class="data"]/tbody/tr/td/text()')

count = 0
for item in items:
    if count == 0:
        currency_list['Цифр. код'] = int(item)
        count +=1
    elif count == 1:
        currency_list['Букв. код'] = item
        count +=1
    elif count == 2:
        currency_list['Единиц'] = int(item)
        count +=1
    elif count == 3:
        currency_list['Валюта'] = item
        count +=1
    elif count == 4:
        currency_list['Курс'] = float(item.replace(',', '.'))
        count = 0
        currencies.append(currency_list)
        currency_list = {}

with open('currencies.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=currencies[0].keys())
    writer.writeheader()
    writer.writerows(currencies)
