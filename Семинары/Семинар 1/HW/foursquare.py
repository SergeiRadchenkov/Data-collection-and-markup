import requests

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

def search_venues(category, location="Москва", limit=5):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Accept": "application/json",
        "Authorization": 'API_KEY'
    }
    params = {
        "query": category,
        "near": location,
        "limit": limit
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Ошибка при запросе:", response.status_code, response.text)
        return None
    

category = input("Введите категорию заведения (например, кофейни, музеи, парки): ")
location = input("Введите местоположение для поиска (например, Москва): ")
limit = int(input("Введите количество результатов для отображения: "))

venues = search_venues(category, location, limit)
    
if venues and "results" in venues:
    for venue in venues["results"]:
        name = venue.get("name", "Название неизвестно")
        location = venue.get("location", {})
        address = location.get("address", "Адрес неизвестен")
        rating = venue.get("rating", "Рейтинг отсутствует")

        print(f"Название: {name}")
        print(f"Адрес: {address}")
        print(f"Рейтинг: {rating}\n")
