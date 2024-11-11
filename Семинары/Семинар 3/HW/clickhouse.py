from clickhouse_driver import Client
import json

client = Client('localhost')

client.execute('CREATE DATABASE IF NOT EXISTS bookstore')

client.execute('''
CREATE TABLE IF NOT EXISTS bookstore.books (
    title String,
    price Float32,
    stock Int32,
    description String
) ENGINE = MergeTree()
ORDER BY title;
''')

with open('books.toscrape.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

books_data = [
    (
        book.get('title', ''),
        float(book.get('price', 0.0)),
        int(book.get('stock', 0)), 
        book.get('description', '') 
    )
    for book in data
]

client.execute('INSERT INTO bookstore.books (title, price, stock, description) VALUES', books_data)

print("Данные успешно записаны в ClickHouse.")
