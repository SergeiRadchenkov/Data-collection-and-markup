from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)

driver.get("https://www.wildberries.ru/")

time.sleep(2)
input = driver.find_element(By.ID, "searchInput")
input.send_keys('Купальники')
input.send_keys(Keys.ENTER)

# time.sleep(2)

while True:
    # wait = WebDriverWait(driver, 30)
    # cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@id]')))

    while True:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@id]')))

        # cards = driver.find_elements(By.XPATH, '//article[@id]')
        count = len(cards)
        driver.execute_script("window.scrollBy(0, 2000)")
        time.sleep(2)
        cards = driver.find_elements(By.XPATH, '//article[@id]')
        if len(cards) == count:
            break 

    for card in cards:
        price = card.find_element(By.CLASS_NAME, "price__lower-price").text
        name = card.find_element(By.XPATH, "./div/a").get_attribute('aria-label')
        url = card.find_element(By.XPATH, "./div/a").get_attribute('href')
        # card.find_element(By.XPATH, '//ins[@class="price__lower-price"]')
        print(name, price, url)
        
    try:
        button = driver.find_element(By.CLASS_NAME, 'pagination-next').click
        actions = ActionChains(driver)
        actions.move_to_element(button).click()
        actions.perform()
    except:
        break

print()