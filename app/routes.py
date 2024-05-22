from app import app
from flask import render_template, request, redirect, url_for
import requests
import os
from bs4 import BeautifulSoup



def report(action):
    try:
        os.system(f'notify-send {action}')
    except NameError:
        pass




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.jinja')


@app.route('/extract', methods=['POST', 'GET'])
def extract():
    if request.method == 'POST':
        product_id = request.form.get('productID')
        #walidacja
        url = f'https://www.ceneo.pl/{product_id}'
        response = requests.get(url)
        if response.status_code == requests.codes['ok']:
            page = BeautifulSoup(response.text, 'html.parser')
            opinions_count = page.select_one("a.product-review__link > span")
            if opinions_count:
                #ekstrakcja
                report()
            return render_template('extract.html.jinja', error='Produkt o podanym kodzie nie posiada opinii.')
        report(f'{product_id}, {url}, {response}')
        return redirect(url_for('product', product_id=product_id))
    return render_template('extract.html.jinja')

@app.route('/products')
def products():
    return render_template('products.html.jinja')

@app.route('/about')
def about():
    return render_template('about.html.jinja')

@app.route('/products/<product_id>')
def product(product_id):
    return render_template('product.html.jinja', product_id=product_id)