#!/usr/bin/env python3
'''
Just the facts script Python230 lesson 05
'''
import os
import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

APP = Flask(__name__)


def get_fact():
    '''
    This section retrieves text from unkno.com
    '''
    response = requests.get('http://unkno.com')

    soup = BeautifulSoup(response.content, 'html.parser')
    facts = soup.find_all('div', id='content')

    return facts[0].getText()



@APP.route('/')
def home():
    return 'FILL ME!'


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 6787))
    APP.run(host='0.0.0.0', port=PORT)
