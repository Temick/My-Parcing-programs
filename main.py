'''Пример простого парсера, который берёт информацию о всех проводимых мероприятиях на сайте Python'''
from bs4 import BeautifulSoup
import requests as rq
import lxml
import json

meropriatia = []
for i in range(1,5):
    page = rq.get(f'https://www.python.org/events/python-events/?page={i}')
    src = page.text

    soup = BeautifulSoup(src,'lxml')

    lst_silok = []
    lst = soup.find('ul', class_='list-recent-events menu').find_all('a')
    for elem in lst:
        lst_silok.append('https://www.python.org' + elem.get('href'))

    for elem in lst_silok:

        page2 = rq.get(elem)
        src = page2.text

        soup = BeautifulSoup(src, "lxml")

        name = soup.find('article', class_='text').find('h1').text.strip()

        location = soup.find('span', class_='single-event-location').text.strip()

        date = soup.find('h3', class_='single-event-date').text.strip().replace('\n', '')

        ssilka = soup.find('div', class_='event-description').find('a').get('href')

        
        meropriatia.append(
            {
                'Name': name,
                'Location': location,
                'Date': date,
                'Silka': ssilka
            }
        )

with open('data_python_org.json', 'w', encoding='utf-8') as file:
    json.dump(meropriatia, file, indent=4, ensure_ascii=False)

