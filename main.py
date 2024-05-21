from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import datetime

app = Flask(__name__)

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

@app.route('/')
def home():
    return "Welcome to the Stock Price API!"

@app.route('/price/<stock_code>')
def price(stock_code):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    price = real_time_price(stock_code)
    return jsonify({'stock': stock_code, 'price': price, 'timestamp': now})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
