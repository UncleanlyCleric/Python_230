#!/usr/bin/env python3

#pylint: disable=W0611,C0103,C0111
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = b']\x05[\x10\x04+S.\xde45P\xe4T\xd7"\xa6\x7f\xd6\x8f6\xed\xd8\xfe'

@app.route('/add', methods=['GET', 'POST'])
def add():
    # session['total']

    if 'total' not in session:
        session['total'] = 0

    if request.method == 'POST':
        number = int(request.form['number'])
        session['total'] += number

    return render_template('add.jinja2', session=session)

if __name__ == 'main':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
