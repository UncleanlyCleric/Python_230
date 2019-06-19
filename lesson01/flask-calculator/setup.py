#!/usr/bin/env python3
#pylint: disable=W0611,C0103,C0111,R0903

from model import db, SavedTotal

db.connect()
db.create_tables([SavedTotal])
