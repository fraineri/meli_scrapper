from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.post("/search")
def process_search():
    title_search = request.form.get('title_search')
    keywords = request.form.get('keywords')

    title_search = title_search.lower()
    title_search = title_search.replace(' ', '-')

    URL = 'https://listado.mercadolibre.com.ar/' + title_search
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'html.parser')

    
    response_list = []

    publications = soup.find_all('li', class_='ui-search-layout__item')
    for publication in publications:
        title = publication.find('h2', class_='ui-search-item__title')
        price_box_without_discount = publication.find('div', class_='ui-search-price__second-line')
        price = price_box_without_discount.find_next('span', class_='andes-money-amount__fraction')
        
        response = dict()
        response["title"] = title.text
        response["price"] = price.text
        response["words"] = title.text.split()
        response_list.append(response)
    
    return response_list