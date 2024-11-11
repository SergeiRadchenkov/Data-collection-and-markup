from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client['bookstore']
books_collection = db['books']

with open('books.toscrape.json', 'r', encoding='utf-8') as f:
    books_data = json.load(f)

filtered_books = [
    {key: book[key] for key in ['title', 'price', 'stock', 'description'] if key in book}
    for book in books_data
]

if filtered_books:
    books_collection.insert_many(filtered_books)

print("Данные по книгам успешно загружены в MongoDB!")


# Получаем все книги
for book in books_collection.find():
    print(book)

# Получаем первую книгу, которая находится в коллекции
book = books_collection.find_one()
print(book)

# Находим книги с ценой меньше $20
cheap_books = books_collection.find({'price': {'$lt': 20}})
for book in cheap_books:
    print(book)

# Получаем только название и цену книги
for book in books_collection.find({}, {'title': 1, 'price': 1, '_id': 0}):
    print(book)

# Поиск книг в описании которых встречается слово "magic"
magic_books = books_collection.find({'description': {'$regex': 'magic', '$options': 'i'}})
for book in magic_books:
    print(book)

# Обновим цену для книги с определённым названием
books_collection.update_one({'title': 'The Magic Book'}, {'$set': {'price': 15}})

# Установим stock на 10 для всех книг с ценой выше $30
books_collection.update_many({'price': {'$gt': 30}}, {'$set': {'stock': 10}})

# Удалим книгу с определённым названием
books_collection.delete_one({'title': 'The Magic Book'})

# Удалим все книги с ценой меньше $5
books_collection.delete_many({'price': {'$lt': 5}})

# Сортировка книг по цене в порядке убывания
sorted_books = books_collection.find().sort('price', -1)
for book in sorted_books:
    print(book)
