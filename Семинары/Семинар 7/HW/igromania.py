from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)

url = "https://www.igromania.ru/reviews/?page=3"

try:
    driver.get(url)
    time.sleep(5)

    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    reviews  = soup.find_all('div', class_='style_card__ZD6TK knb-card withShadow')

    games = []
    for review in reviews:
        try:
            title = review.find('h3').get_text(strip=True)
            rating = review.find('div', class_='CardLabel_label__JCFKT').get_text(strip=True)
            games.append({'title': title, 'rating': rating})
        except AttributeError:
            continue 

    with open('games.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'rating']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(games)

    print("Данные успешно извлечены и сохранены в 'games.csv'.")

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()
