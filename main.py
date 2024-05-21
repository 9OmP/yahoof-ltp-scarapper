import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import datetime
from requests.exceptions import ConnectionError

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('span')
        texts = []
        texts.append(spans[0].getText())
    except IndexError:
        texts = []
    return texts

def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code
    # print(url)
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'container svelte-aay0dk')
        if texts != []:
            price= texts[0]
        else:
            price = []
    except ConnectionError:
        price
    return price

Stock = ['BTC-USD']

while True:
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print("Current price of", Stock[0], "is:", real_time_price(Stock[0]), f"at {now}")
    time.sleep(30)  # Fetch data every x seconds