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
    This will send the aforementioned fact to the translation application
    '''
    url = 'https://hidden-journey-62459.herokuapp.com'
    payload = {'input_text': fact}
    request_return = requests.post(url, data=payload, allow_redirects=False)
    # new_page = request_return.headers['Location']
    new_page = request_return.text

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

# https://hidden-journey-62459.herokuapp.com

'''
eve:ustjay-ethay-actsfayig jmiller$ python main.py
 * Tip: There are .env files present. Do "pip install python-dotenv" to use them.
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:6787/ (Press CTRL+C to quit)
[2019-07-17 11:58:10,186] ERROR in app: Exception on / [GET]
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 2292, in wsgi_app
    response = self.full_dispatch_request()
  File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1815, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1718, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/usr/local/lib/python3.7/site-packages/flask/_compat.py", line 35, in reraise
    raise value
  File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1813, in full_dispatch_request
    rv = self.dispatch_request()
  File "/usr/local/lib/python3.7/site-packages/flask/app.py", line 1799, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "main.py", line 114, in home
    new_page = get_page(fact)
  File "main.py", line 103, in get_page
    new_page = request_return.headers["Location"]
  File "/usr/local/lib/python3.7/site-packages/requests/structures.py", line 54, in __getitem__
    return self._store[key.lower()][1]
KeyError: 'location'
127.0.0.1 - - [17/Jul/2019 11:58:10] "GET / HTTP/1.1" 500 -
'''
