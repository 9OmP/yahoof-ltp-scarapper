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
    url = f'https://finance.yahoo.com/quote/{stock_code}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        r = requests.get(url, headers=headers)
        #print(r)  # Check response
        if r.status_code == 404:
            return "Page not found"
        elif r.status_code != 200:
            return f"Error fetching data: HTTP {r.status_code}"

        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'container svelte-aay0dk')
        #print(texts)  # Debug: print the texts extracted
        return texts[0] if texts else "Price not found"
    except ConnectionError:
        return "Failed to connect"


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
