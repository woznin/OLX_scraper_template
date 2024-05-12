from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def load(url):
    page = requests.get(url)
    sup1 = BeautifulSoup(page.content, "html.parser")
    sup2 = BeautifulSoup(sup1.prettify(), "html.parser")
    return sup2


def get_data(kod, url):
    try:
        title = kod.find_all('h4')[1].text.strip()
        price = kod.find_all('h3')[1].text.strip()
    except IndexError:
        return
    link = url
    title = title.lower()
    price = price.lower()
    index_temp = title.find("iphone")
    index_temp2 = title.find("gb")
    title = title[index_temp:index_temp2 + 2]
    if title == '':
        return
    else:
        return title, price, link


list_ = ['']
base_url = 'https://www.olx.pl'
all_data = []

for i in range(2, 16):
    list_.append(f'?page={i}')

for j in list_:
    URL = f'https://www.olx.pl/elektronika/telefony/q-iphone/{j}'
    print(URL)
    cc = load(URL)
    hrefs_all = cc.findAll('a', href=re.compile('/d/oferta/'))
    print(len(hrefs_all))

    for i in hrefs_all:
        x = i.get('href')
        URL = base_url+x
        cc = load(URL)
        ones_data = get_data(cc, URL)
        if ones_data is not None:
            all_data.append(ones_data)

columns = ['model', 'cena', 'link']
df = pd.DataFrame(all_data, columns=columns)
df.to_csv('phones.csv')
