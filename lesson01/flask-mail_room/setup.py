#!/usr/bin/env python3
'''
Building the default database and populating it.
'''
import random
from model import DB, Donor, Donation

# pylint: disable = C0103

DB.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
DB.drop_tables([Donor, Donation])

DB.create_tables([Donor, Donation])

alice = Donor(name="Alice")
alice.save()

bob = Donor(name="Bob")
bob.save()

charlie = Donor(name="Charlie")
charlie.save()

donors = [alice, bob, charlie]

for x in range(30):
    Donation(donor=random.choice(donors), value=random.randint(100, 10000)).save()
