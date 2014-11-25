from textblob import TextBlob
import numpy as np
import re

CLASSIFY_SENSITIVITY = 3
CLASSIFY_SENSITIVITY_EXP = 3
CLASSIFY_SENSITIVITY_OFFSET = 0.05
def remove_punctuation(text):
    return re.sub(r'[^A-Za-z0-9 ]', "", text)

def read_sentimentList(file_name):
    ifile = open(file_name, 'r')
    happy_log_probs = {}
    sad_log_probs = {}
    ifile.readline() #Ignore title row
    
    for line in ifile:
        tokens = line[:-1].split(',')
        happy_log_probs[tokens[0]] = float(tokens[1])
        sad_log_probs[tokens[0]] = float(tokens[2])

    ifile.close()

    return happy_log_probs, sad_log_probs

happy_log_probs, sad_log_probs = read_sentimentList('twitter_sentiment_list.csv')

def translate_result(x):
    
    return 10 / (1 + np.exp(-CLASSIFY_SENSITIVITY_EXP * (x - CLASSIFY_SENSITIVITY_OFFSET)))
    return (x+1)*5

def classify_sentiment(tweet):
    blob = TextBlob(tweet)
    sentence_polarities = []
    for sentence in blob.sentences:
        sentence_polarities.append(sentence.sentiment.polarity)
    median = np.median(sentence_polarities)
    
    return int(round(translate_result(median)))

def classify_sentiment2(words, l_happy_log_probs, l_sad_log_probs):
    # Get the log-probability of each word under each sentiment
    happy_probs = [l_happy_log_probs[word] for word in words if word in l_happy_log_probs]
    sad_probs = [l_sad_log_probs[word] for word in words if word in l_sad_log_probs]

    # Sum all the log-probabilities for each sentiment to get a log-probability for the whole tweet
    try:
        tweet_happy_log_prob = np.sum(happy_probs) / len(happy_probs)
        tweet_sad_log_prob = np.sum(sad_probs) / len(sad_probs)

        tweet_happy_log_prob = np.min(happy_probs)
        tweet_sad_log_prob = np.min(sad_probs)
        
        # Calculate the probability of the tweet belonging to each sentiment
        prob_happy = np.reciprocal(np.exp(CLASSIFY_SENSITIVITY * (tweet_happy_log_prob-tweet_sad_log_prob)) + 1)
        
        prob_sad = 1 - prob_happy
    
        #return int(round(prob_happy*10))#, prob_sad*10
        return int(10 * prob_happy)
    except:
        return 5

def classify_tweet(tweet):
    happy_prob = classify_sentiment(tweet)
    return happy_prob
    
def classify_tweet2(tweet):
    tweet_array = process_tweet(tweet)
    happy_prob = classify_sentiment2(tweet_array, happy_log_probs, sad_log_probs)
    return happy_prob
    
def process_tweet(tweet):
    processed = tweet.lower()
    processed = remove_punctuation(processed) + ' ' + tweet
    return processed.split(' ')

