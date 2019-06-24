#!/usr/bin/env python3
'''
Modelling for the donor collection in flask-mailroom
'''
import os

# pylint: disable = R0903
from peewee import Model, CharField, IntegerField, ForeignKeyField
from playhouse.DB_url import connect

DB = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.DB'))

class Donor(Model):
    '''
    Modelling the donor field, it's pretty simple.  I had to change the
    unique to False in order for the donation collection to work correctly.
    '''
    name = CharField(max_length=255, unique=False)

    class Meta:
        '''
        Defining database for donors.
        '''
        database = DB

class Donation(Model):
    '''
    Modelling the donation field.
    '''
    value = IntegerField()
    donor = ForeignKeyField(Donor, backref='donations')

    class Meta:
        '''
        Defining database for everything else.
        '''
        database = DB
