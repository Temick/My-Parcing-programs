'''Пример простого парсера сайта https://stagestandup.ru/, который берёт информацию о проводимых мероприятия, ссылки на мероприятие
    и формирует json-файл 'standup.json' с этими данными'''
from bs4 import BeautifulSoup
import requests as rq
import json
from selenium import webdriver
import time
import undetected_chromedriver

url = 'https://stagestandup.ru/'

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.1.714 Yowser/2.5 Safari/537.36")

driver = webdriver.Chrome(executable_path=r'C:\Users\Artyom\Desktop\Parsing\chromedriver.exe', options=options)

driver.get(url=url)
time.sleep(10)
with open('index2.html','w',encoding='utf-8') as file:
    file.write(driver.page_source)
time.sleep(5)
driver.close()
driver.quit()

with open('index2.html',encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src,"lxml")
divs = soup.find_all('div',class_='t-card__btntext-wrapper')
urls = []
for elem in divs:
    if 'SOLD OUT' in elem.text:
        continue
    else:
        if len(str(elem.find('a').get('href'))) < 30:
            urls.append('https://stagestandup.ru' + str(elem.find('a').get('href')).replace('#ticketscloud:event=',''))
        else:
            urls.append('https://ticketscloud.com/v1/widgets/common?event=' + str(elem.find('a').get('href')).replace('#ticketscloud:event=',''))

meropriatia = []
for url in urls:
    if len(url) > 100:
        driver = undetected_chromedriver.Chrome()
        driver.get(url=url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,"lxml")
        if soup.find('div',class_='header__event-title'):
            name = soup.find('div',class_='header__event-title').text
            meropriatia.append(
                {
                    "Name": name,
                    "URL": url
                }
            )
            driver.close()
            driver.quit()
        else:
            driver.close()
            driver.quit()
            continue
    else:
        driver = undetected_chromedriver.Chrome()
        driver.get(url=url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,"lxml")
        name = soup.find('title').text
        meropriatia.append(
            {
                "Name": name,
                "URL": url
            }
        )
        driver.close()
        driver.quit()

with open('standup.json', 'w', encoding='utf-8') as file:
    json.dump(meropriatia,file,indent=4,ensure_ascii=False)











