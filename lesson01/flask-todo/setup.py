#!/usr/bin/env python3.7
'''
Scripts to run to set up our database
'''
from datetime import datetime
from model import db, User, Task


# Create the database tables for our model
db.connect()
db.drop_tables([User, Task])
db.create_tables([User, Task])

Task(name='Do the laundry.').save()
Task(name='Do the dishes.', performed=datetime.now()).save()
