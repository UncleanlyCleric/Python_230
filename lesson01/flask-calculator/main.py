#!/usr/bin/env python3

#pylint: disable=W0611,C0103,C0111
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.jinja2')

if __name__ == 'main':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
