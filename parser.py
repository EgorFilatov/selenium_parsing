import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
import time
from selenium.webdriver.common.by import By
import cfscrape
import csv
import os


link = 'https://www.g2.com/categories?utf8=✓&q%5Bsearch_query_cont%5D=&q%5Bcategory_type_eq%5D=software'
FILE = 'g2_information.csv'


def page_code(link):
    driver = webdriver.Chrome()
    driver.get(link)
    page_code = driver.page_source
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return page_code


def get_pages_count():
    html = page_code('https://www.g2.com/categories/pricing')

    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='pagination__named-link js-log-click')
    last_page_link = pagination[1].get('href')
    pages_count_start = last_page_link.find("page=") + 5
    pages_count_end = last_page_link.find("#")
    pages_count = last_page_link[pages_count_start:pages_count_end]
    print(pages_count)



def main_page_information(page_code):
    soup = BeautifulSoup(page_code, 'html.parser')
    items = soup.find_all('ul', class_='list list--spaced list--spaced--with-divider feature-box__list')
    information = []
    for el in items:
        categories = el.find_all('a')
        for el in categories:
            information.append({
                'category_name': el.get_text(strip=True),
                'link': 'https://www.g2.com' + el.get('href')
            })
    return information


def categories_page_information(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='paper pt-half pb-0 my-1 x-ordered-events-initialized')
    if soup.find('a', text='Next ›'):
        next_page = soup.find('a', text='Next ›').get('href')
    else:
        next_page = 0
    information = []
    for el in items:
        company_information = el.find('span', class_='product-listing__paragraph').get_text(strip=True).replace('\n\n', ' ').replace('...Show More', ' ').replace('\n', '') + el.find('span', class_='product-listing__paragraph').get('data-truncate-revealer-overflow-text').replace('\n\n', ' ').replace('\n', '')
        information.append({
            'company_name': el.find('div', class_='product-listing__product-name').get_text(strip=True),
            'company_information': company_information,
            'next_page': next_page,
        })
    return information


def save_file(items_information, cat, path):
    with open(path, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['CATEGORY', 'COMPANY NAME', 'COMPANY INFORMATION'])
        for el in items_information:
            writer.writerow([cat, el['company_name'], el['company_information']])


def add_to_file(items_information, cat, path):
    with open(path, 'a', encoding='utf8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for el in items_information:
            writer.writerow([cat, el['company_name'], el['company_information']])


def parsing():
    html = page_code(link)
    main_information = main_page_information(html)
    i = 0
    for el in main_information:
        html = page_code(el['link'])
        category = el['category_name']
        categories_information = categories_page_information(html)
        if i == 0:
            save_file(categories_information, category, FILE)
            while categories_information[0]['next_page']:

                html = page_code(categories_information[0]['next_page'])
                categories_information = categories_page_information(html)
                print('func_end= ', categories_information)
                if len(categories_information) == 0:
                    break
                add_to_file(categories_information, category,FILE)
            i = 1
        else:
            add_to_file(categories_information, category,FILE)
            while categories_information[0]['next_page']:

                html = page_code(categories_information[0]['next_page'])
                categories_information = categories_page_information(html)
                print('func_end= ', categories_information)
                if len(categories_information) == 0:
                    break
                add_to_file(categories_information, category,FILE)






parsing()
