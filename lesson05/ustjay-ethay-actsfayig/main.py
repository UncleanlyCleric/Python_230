#!/usr/bin/env python3
'''
Just the facts script Python230 lesson 05
'''
# pylint: disable=C0103
import os
import requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)


def template():
    '''
    Formatting template for web page.
    '''
    page_template = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>Pig Latin / Fact Mashup</title>
  </head>
  <body>
  <div class="p-4 container-fluid">
    <h1>Pig Latin / Fact Mashup</h1><br>
    <div class="card-deck">
    <div class="card">
        <img src="https://media.giphy.com/media/3o7btQDFlvGcv8PXt6/giphy.gif" class="card-img-top" alt="fact">
        <div class="card-body">
        <h5 class="card-title">Random Fact</h5>
        <p class="card-text">{}</p>
        <a class="btn btn-secondary" href="/" role="button">Another fact?</a>
        </div>
    </div>
    <div class="card">
        <img src="https://i.imgur.com/33Pa2Rr.png" class="card-img-top" alt="Farnsworth">
        <div class="card-body">
        <h5 class="card-title">Translation Page</h5>
        <p class="card-text">{}</p>
        <a class="btn btn-secondary" href="{}" role="button">Go to translation</a>
        </div>
    </div>
    <div class="card">
        <img src="https://i.imgur.com/zg84CLC.jpg" class="card-img-top" alt="pigs (three different ones)">
        <div class="card-body">
        <h5 class="card-title">Fact in Pig Latin</h5>
        <p class="card-text">{}</p>
        <a class="btn btn-secondary" href="https://en.wikipedia.org/wiki/Pig_Latin" role="button">Learn about Pig Latin</a>
        </div>
    </div>
    </div>
    <br>
    <br>
  </body>
</html>
'''
    return page_template


def get_fact():
    '''
    This section retrieves a fact from unkno.com
    '''
    response = requests.get('http://unkno.com')

    soup = BeautifulSoup(response.content, 'html.parser')
    facts = soup.find_all('div', id='content')

    fact = facts[0].getText()

    # Fun little formatting issue here.
    fact = fact.replace("â€™", "'").replace("â€œ", '"').replace('â€”', "—").\
    replace("â€", '"')

    return fact


def get_page(fact):
    '''
    This will send the aforementioned fact to the translation application.
    Initially I had a problem of 405 and 500 errors with this section,
    it turned out, I needed to add the piglatinize directory to the URL
    '''
    url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'
    payload = {'input_text': fact}
    request_return = requests.post(url, data=payload, allow_redirects=False)
    new_page = request_return.headers['Location']

    return new_page


def get_translation(new_page):
    '''
    Ultimately, this is the function that translates to pig latin.
    '''
    response = requests.get(new_page)
    soup = BeautifulSoup(response.content, 'html.parser')

    fact = soup.find('body').getText()
    strip_fact = fact.replace('Pig Latin\nEsultray', '')

    return strip_fact


@app.route('/')
def home():
    '''
    Web application home page.
    '''
    fact = get_fact().strip()
    new_page = get_page(fact)
    translation = get_translation(new_page)

    return template().format(fact, new_page, new_page, translation)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 6787))
    app.run(host='0.0.0.0', port=PORT)

'''
App at https://nameless-shore-99856.herokuapp.com/
'''
