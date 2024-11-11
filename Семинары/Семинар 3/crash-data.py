import json
from pymongo import MongoClient

# with open('crash-data.json', 'r', encoding='utf-8') as file:
#    data = json.load(file)

# json_data_as_bytes = json.dumps(data).encode('utf-8')

# with open('data.json', 'wb') as f:
#     f.write(json_data_as_bytes)


client = MongoClient('localhost', 27017)
db = client['crashes']
info = db.info

info.delete_many({})

with open('data.json', 'r') as f:
    data = json.load(f)

count_duplicated = 0

for feature in data['features']:
    _id = feature.get('properties').get('tamainid')
    feature['_id'] = _id
    try:
        info.insert_one(feature)
    except:
        count_duplicated += 1
        print(feature)

print(count_duplicated)


# for doc in info.find({'properties.lat2': {'$gt': 35.0, '$lt': 36.0}, 'properties.lon2': {'$gt': -78, '$lt': -77}}):
#     print(doc)
#     print()

# for doc in info.find({'$and': [{'properties.lat2': {'$gt': 35.0, '$lt': 36.0}}, {'properties.vehicle2': 'PASSENGER CAR'}]}):
#    print(doc)
