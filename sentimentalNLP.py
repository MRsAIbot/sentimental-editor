'''
Created on 22 Nov 2014

@author: hadoop
'''
from ttp import ttp
from random import randrange
from compute_sentiment import classify_tweet

from topic_count import article_keywords

def articleKeywords(article, title, n):
    article_plus = '%s %s %s %s' % (article, title, title, title)
    return article_keywords(article_plus, n)

def sentiment(tweet):
    return classify_tweet(tweet['clean_text'])

def cleanTweet(tweet):
    p = ttp.Parser()
    result = p.parse(tweet)
    
    clean = tweet.replace('#','')
    for url in result.urls:
        clean = clean.replace(url,'')
    
    return clean