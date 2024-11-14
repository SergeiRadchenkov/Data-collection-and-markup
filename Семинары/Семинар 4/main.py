from lxml import html
import requests
from pprint import pprint as pp

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36'}

url = 'https://www.ebay.com'

response = requests.get(url + '/b/Fishing-Equipment-Supplies/1492/bn_1851047?_trkparms=parentrq%3A2202ad5c1930a62307fb85c4ffffcca8%7Cpageci%3A9c285442-a132-11ef-8cf7-9e06035131a9%7Cc%3A4%7Ciid%3A1%7Cli%3A8874', headers=header)
dom = html.fromstring(response.text)

item_list = []
items = dom.xpath("//ul[@class='brwrvr__item-results brwrvr__item-results--list']/li")
for item in items:
    item_info = {}

    name = item.xpath(".//h3[@class='textual-display bsig__title__text']/text()")
    link = item.xpath(".//span[@class='bsig__title']/a/@href")
    price = item.xpath(".//span[@class='textual-display bsig__price bsig__price--displayprice']/text()")
    add_info = item.xpath(".//span[@class='textual-display negative']/text()")

    item_info['name'] = name
    item_info['link'] = link
    item_info['price'] = price
    item_info['add_info'] = add_info
    item_list.append(item_info)


pp(item_list)
