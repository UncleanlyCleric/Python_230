#!/usr/bin/env python3
#pylint: disable=W0611,C0103,C0111,R0903

import os
from peewee import Model, CharField, IntegerField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_IRL', 'sqlite:///my_database.db'))

class SavedTotal(Model):
    code = CharField(max_length=255, unique=True)
    value = IntegerField()

    class Meta:
        database = db
