#!/usr/bin/env python3

#pylint: disable=W0611,C0103,C0111
import os
import base64
from flask import Flask, render_template, request, redirect, url_for, session
from model import SavedTotal


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


@app.route('/save', methods=['POST'])
def save():
    total = session.get('total', 0)
    code = base64.b32encode(os.urandom(8)).decode().strip('=')

    saved_total = SavedTotal(value=total, code=code)
    saved_total.save()

    return render_template('save.jinja2', code=code)


@app.route('/retrieve')
def revtrieve():
    code = request.args.get('code', None)

    '''
    If the user is visiting this page, but has no submit it will just render
    the retrieve.jinja2 template.

    If they DID submit the form, it will attempt to retrieve the SavedTotal that
    has the provided code, then save the total from that SavedTotal into
    session['total'].  After this, it will redirect back to add
    '''

    if code is None:
        return render_template('retrieve.jinja2')
    # else:
    try:
        saved_total = SavedTotal.get(SavedTotal.code == code)
    except SavedTotal.DoesNotExist:
        return render_template('retrieve.jinja2', error="Code not found.")
    session['total'] = saved_total.value

    return redirect(url_for('add'))


if __name__ == 'main':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
