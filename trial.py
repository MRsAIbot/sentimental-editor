
'''
Created on 28 Mar 2014

@author: hadoop
'''
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

app = Flask(__name__)


INSTAGRAM_CLIENT_ID = '7e2dae311a9d433184472ff49cc7f3f8'
INSTAGRAM_CLIENT_SECRET = '49355d81374645549cbbe11dcb8ca78a'

# TWITTER KEYS 1.1

CONSUMER_KEY = 'sAF9dsiydz6mggIXXDtCw4AC9' 
CONSUMER_SECRET = 'Va4scLJ2Pb44PrJryhpFpYOBbMqJCqi5mPdmt8EIesunONmXxq'
ACC_TOKEN = '2161311224-bCu9r7r9lh4wO7fezqt0DtvLn76A61EcetVrlMK'
ACC_SECRET = 'IqeskxVA0L5ah2daadv5qNAFchX24RS9uvgTcHpkhLNZe'

import tweepy
import json
from instagram.client import InstagramAPI

instApi = InstagramAPI(client_id=INSTAGRAM_CLIENT_ID, client_secret=INSTAGRAM_CLIENT_SECRET)

twitAuth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
twitAuth.set_access_token(ACC_TOKEN, ACC_SECRET)
twitApi = tweepy.API(twitAuth)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/keywords/')
def keywords():
    phrases = [{'phrase':'President Obama', 'sentiment': 0}, 
               {'phrase':'Conde Nast', 'sentiment': 1}]
    return json.dumps(phrases)



def getInstagram(tag):
    media_search = instApi.tag_recent_media(tag_name = tag, count = 3)
    media_results = []
    for media in media_search[0]:
        user = media.user
        images = media.images
        low_res = images['low_resolution']
        media_results.insert(0, {
                             'created_at':media.created_time.strftime("%H:%M:%S %A"),
                             'url': low_res.url,
                             'username': user.username
                             })
    return media_results

def getInstagrams(tags):
    instagrams = []
    for tag in tags:
        results = getInstagram(tag)
        for result in results:
            instagrams.append(result)
    return instagrams

if __name__ == '__main__':
    text = ""
    print getInstagrams(['monkeys','food'])