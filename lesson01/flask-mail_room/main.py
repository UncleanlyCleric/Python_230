#!/usr/bin/env python3

#pylint: disable=W0611,C0103,C0111

import os
import base64
import peewee
from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('list_all'))


@app.route('/donations/')
def list_all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/add/', methods=['GET', 'POST'])
def add_donation():
    try:
        if request.method == 'POST':
            new_donor = Donor(name=request.form['donor'])
            new_donor.save()
            donation = Donation(donor=new_donor, value=request.form['value'])
            donation.save()
            return redirect(url_for('list_all'))
        return render_template('add.jinja2')

    except peewee.IntegrityError as e:
        print('{} already exists'.format('new_donor' in e.args))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
