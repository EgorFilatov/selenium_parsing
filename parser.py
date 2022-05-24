import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import cfscrape
import csv
import os


driver = webdriver.Chrome()
driver.get('https://www.g2.com/categories?utf8=✓&q%5Bsearch_query_cont%5D=&q%5Bcategory_type_eq%5D=software')
page_code = driver.page_source

soup = BeautifulSoup(page_code, 'html.parser')
items = soup.find_all('ul', class_='list list--spaced list--spaced--with-divider feature-box__list')
categories = []
for el in items:
    categories.append({
        'category_name': el.find('li', class_='vertical--xlarge link').get_text(strip=True),
        'link': el.find('a', class_='tm-article-snippet__title-link').get('href')
    })

print(categories)





