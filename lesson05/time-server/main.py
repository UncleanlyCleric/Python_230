#!/usr/bin/#!/usr/bin/env python3
'''
Python 230 Lesson 05 activity:  Epoch time microserver
'''
import os
import time
from flask import Flask

APP = Flask(__name__)

@APP.route("/")
def get_time():
    '''
    This will get the current epoch time.
    '''
    current_time = int(time.time())
    return str(current_time)

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 6738))
    APP.run(host="0.0.0.0", port=PORT)
