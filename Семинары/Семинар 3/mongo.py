from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import *

client = MongoClient('localhost', 27017)
db = client['users']
# db2 = client['books']
persons = db.persons
duplicates = db.duplicates

doc = {'_id': '32321321dghrtbrtrt',
       'author': 'Peter',
       'age': 38,
       'text': 'is cool! Wildberry',
       'tags': ['cool', 'hot', 'ice'],
       'date': '14.06.1983'}

try:
    persons.insert_one(doc)
except DuplicateKeyError as e:
    print(e)





authors_list = [{'author': 'John',
                 'age': 29,
                 'text': 'Too bad! Strawberry',
                 'tags': 'ice',
                 'date': '04.08.1971'},
                 {'_id': 123,
                  'author': 'Anna',
                  'age': 36,
                  'title': 'Hot Cool!!!',
                  'text': 'easy too!',
                  'date': '26.01.1995'},
                  {'author': 'Jane',
                  'age': 43,
                  'title': 'Nice book',
                  'text': 'Pretty text not long',
                  'date': '08.08.1975',
                  'tags': ['fantastic', 'criminal']}]

# for author in authors_list:
#    try:
#        persons.insert_one(author)
#    except DuplicateKeyError as e:
#        duplicates.insert_one(author)

# persons.insert_many(authors_list)

for doc in persons.find({'$or': [{'author': 'Peter'}, {'age': 29}]}):
    pprint(doc)
    print()

for doc in persons.find({'age': {'$gt': 30}}):
    pprint(doc)
    print()

for doc in persons.find({'$or': [{'author': 'Peter'}, {'age': {'$gt': 30}}]}):
    pprint(doc)
    print()

for doc in persons.find({'author': {'$regex': 'J.'}}, {'_id': 0}).sort('age', -1):
    pprint(doc)
    print()

persons.update_one({'author': 'Peter'}, {'$set': {'author': 'Petya'}})

new_data = {
    'author': 'Andrew',
    'age': 28,
    'text': 'is not!',
    'date': '11.09.1991'
}

persons.update_one({'author': 'Peter'}, {'$set': new_data})

persons.replace_one({'author': 'Andrew'}, new_data)

persons.delete_one({'author': 'Peter'})
persons.delete_many({'author': 'Peter'})


for doc in persons.find():
    print(doc)
