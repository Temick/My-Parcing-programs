'''Пример простого парсера сайта "www.championat.com", который берёт данные о футбольных матчах
    и записывает их в json-файл "footbal.json"'''
import requests as rq
from bs4 import BeautifulSoup
from datetime import date
import json

t = date.today()

url = f'https://www.championat.com/stat/football/#{str(t)}'

headears = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.714 Yowser/2.5 Safari/537.36"
}

req = rq.get(url=url, headers=headears)

with open('index.html','w',encoding='utf-8') as file:
    file.write(req.text)

with open('index.html', encoding='utf-8') as file:
    res = file.read()

soup = BeautifulSoup(res,'lxml')


divs = soup.find_all('li',class_='seo-results__item')
meropriatia = []
for elem in divs:
    name_match_and_results = elem.find('a').text
    time_match = elem.find('span',class_='seo-results__item-date').text
    status_math = elem.find('span',class_='seo-results__item-status').text
    url_match = 'https://www.championat.com' + str(elem.find('a').get('href'))
    meropriatia.append(
        {
            "NameMatchAndResult": name_match_and_results,
            "TimeMatch": time_match,
            "StatusMatch": status_math,
            "URL_Match": url_match
        }
    )

with open('footbal.json','w',encoding='utf-8') as file:
    json.dump(meropriatia,file,indent=4,ensure_ascii=False)


