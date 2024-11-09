import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint

ua = UserAgent()

#url = 'https://www.boxofficemojo.com/intl/?ref_=bo_nb_hm_tab'
url = 'https://www.boxofficemojo.com'

headers = {'User-Agent': ua.chrome}
params = {'ref_': 'bo_nb_hm_tab'}

session = requests.session()

response = session.get(url+'/intl', params=params, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
# test_link = soup.find('a', {'class': 'a-link-normal'})
rows = soup.find_all('tr')

films = []

for row in rows[2:-3]:
    film = {}

    # area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).find('a')
    area_info = row.find('td', {'class': 'mojo-field-type-area_id'}).findChildren()[0]
    film['area'] = [area_info.getText(), url + area_info.get('href')]

    weekend_info = row.find('td', {'class': 'mojo-field-type-date_interval'}).findChildren()[0]
    film['weekend'] = [area_info.getText(), url + weekend_info.get('href')]

    film['releases'] = int(row.find('td', {'class': 'mojo-field-type-positive_integer'}).getText())

    frelease_info = row.find('td', {'class': 'mojo-field-type-release'}).findChildren()[0]
    film['frelease'] = [frelease_info.getText(), url + frelease_info.get('href')]

    try:
        distributor_info = row.find('td', {'class': 'mojo-field-type-studio'}).findChildren()[0]
        film['distributor'] = [distributor_info.getText(), url + distributor_info.get('href')]
    except: 
        print('Exception with frelease, object = ', film['frelease'])
        film['distributor'] = None

    film['gross'] = int(row.find('td', {'class': 'mojo-field-type-money'}).getText().replace("$", "").replace(",", ""))

    films.append(film)
 
pprint(films)
