
'''
Created on 28 Mar 2014

@author: hadoop
'''
# -*- coding: utf-8 -*-
from sentimentalNLP import articleKeywords
from sentimentalNLP import sentiment
from sentimentalNLP import cleanTweet
from numpy import median


from flask import Flask, render_template
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
def renderSentimental():
    return render_template('index.html')

@app.route('/keywords/')
def keywords():
    phrases = [{'phrase':'President Obama', 'sentiment': 0}, 
               {'phrase':'Conde Nast', 'sentiment': 1}]
    return json.dumps(phrases)

@app.route('/search/<keywords>')
def getStatus(keywords = None):
    return getTwitter(keywords)
    
def getTwitter(keywords):
    searchString = '+'.join(keywords)
    searchString = searchString.replace(' ', '+')
    try:
        results = twitApi.search(q = searchString, lang = 'en')
        statuses = []
        for result in results:
            statuses.append(statusSimple(result))
        return statuses
    except tweepy.TweepError:
        return {'error': 'TwitterError'}
    except:
        return {'error': 'GeneralError'}
    
 
    
@app.route('/singleKeyword/<keyword>')
def getSingle(keyword):
    try:
        results = twitApi.search(q = keyword, lang = 'en')
        statuses = []
        for result in results:
            statuses.append(statusSimple(result))
        return statuses
        
    except tweepy.TweepError:
        return {'error': 'TwitterError'}
    except:
        return {'error': 'GeneralError'}

@app.route('/PostTest/', methods = ['GET', 'POST'])
def getPostTest():
    if request.method == 'POST':
        try:
            article = request.form['article']
        except:
            article = ''
        
        try:
            title = request.form['title']
        except:
            title = ''
    return json.dumps({'title':title, 'article':article})


@app.route('/sentimental/', methods = ['GET', 'POST'])
def getSentimental():
    if request.method == 'POST':
        try:
            article = request.form['article']
        except:
            article = ''
        
        try:
            title = request.form['title']
        except:
            title = ''
    else:
        article = 'read article from post request'
        title = 'obama article'
        
    keywords = articleKeywords(article, title, 5) 
    
    tweets = getTwitter(keywords[0:2])
    for tweet in tweets:
        tweet['sentiment'] = sentiment(tweet)
    
    instagrams = getInstagrams(keywords)
    
    keywords = keywordWithSentiment(keywords)
    

    
    sentimentalObject = {'keywords': keywords, 'tweets': tweets, 'instagrams':instagrams}
    
    return json.dumps(sentimentalObject)

@app.route('/getpersonbyid', methods = ['POST'])
def getPersonById():
    personId = int(request.form['personId'])
    return str(personId)

def statusSimple(status):
    user = status.user
    statusObject = {'text': status.text, 'user': user.screen_name, 
                    'created': status.created_at.strftime("%H:%M:%S %A"), 'name': user.name,
                    'clean_text': cleanTweet(status.text),
                    'profile_image':user.profile_image_url }
    
    statusObject['name'] = statusObject['name'].replace('\n',' ')
    statusObject['text'] = statusObject['text'].replace('\n',' ')
    statusObject['clean_text'] = statusObject['clean_text'].replace('\n',' ')
#    statusObject = {'text': status.text, 'user': status.user.screen_name, 'name': status.user.username, 'created': status.created_at}
    
    return statusObject

def keywordWithSentiment(keywords):
    results = [];
    for keyword in keywords:
        results.append({'phrase':keyword, 'sentiment': keywordSentiment(keyword)})
    return results

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    return sortedLst[index]

    
def keywordSentiment(keyword):
    #download tweets
    try:
        tweets = getSingle(keyword)

        if len(tweets) > 0:
            s = [sentiment(tweet) for tweet in tweets]
            return median(s)
        else:
            return 2
    except:
        return 8

def getInstagram(tag):
    media_search = instApi.tag_recent_media(tag_name = tag, count = 4)
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
    app.run(debug=True)