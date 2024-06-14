from app import app
from flask import render_template, request, redirect, url_for
import requests
import os
from bs4 import BeautifulSoup
from app import utils
import json



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
            all_opinions = []
            for opinion in opinions:
                single_opinion = {
                    key: utils.get_data(opinion, *value)
                        for key, value in utils.selectors.items()
                }
                all_opinions.append(single_opinion)
                if not os.path.exists("app/data"):
                    os.mkdir("app/data")
                if not os.path.exists("app/data/opinions"):
                    os.mkdir("app/data/opinions")
                jf = open(f'app/data/opinions/{product_id}.json', 'w', encoding='UTF-8')
                json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
                jf.close()
                return redirect(url_for('product', product_id=product_id))
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

@app.route('/product/<product_id>')
def product(product_id):
    if not os.path.exists('app/data/opinions'):
        return redirect(url_for('extract'))
    jf = open(f'app/data/opinions/{product_id}.json', 'r', encoding='UTF-8')
    opinions = json.load(jf)
    jf.close()
    return render_template('product.html.jinja', product_id=product_id)