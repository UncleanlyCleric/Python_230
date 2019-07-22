#!/usr/bin/env python3
'''
github user query script.
Interacts with the API for github to query and display requests associated with
a username passed to sys.argv
'''
# pylint: disable = C0103

import sys
import json

import requests

# Use Like python githubber.py JASchilz
# (or another user name)

if __name__ == "__main__":
    username = sys.argv[1]

    '''
    Retrieves a list of events associated with the stated username.
    '''
    response = requests.get('https://api.github.com/users/{}/events'.format(username))
    events = json.loads(response.content)

    '''
    Prints the timestamp of the first event in the list.
    '''
    print(events[0]['created_at'])
