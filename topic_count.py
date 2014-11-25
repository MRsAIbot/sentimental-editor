from collections import Counter, defaultdict
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem import SnowballStemmer as SS
import nltk
import string

import re

def remove_punctuation(text):
	return re.sub(r'[^A-Za-z0-9 ]', "", text)
   
def get_tokens(text):
	lower = text.lower()
	no_punctuation = remove_punctuation(lower)
	tokens = nltk.word_tokenize(no_punctuation)
	return tokens

def article_keywords(article, n):
	tokens = get_tokens(article)
	return return_n_keywords(tokens, n)

# Takes an array of tokens and an integer, n. Computes the n most frequently occurring tokens.
def return_n_keywords(tokens, n):
	stemmer = SS('english')
	filtered = [w for w in tokens if not w in stopwords.words('english')]
	counts = defaultdict(int)

	for word in filtered:
		stem = stemmer.stem(word)
		if stem in counts:
			shortest,count = counts[stem]
			if len(word) < len(shortest):
				shortest = word
			counts[stem] = (shortest, count+1)
		else:
			counts[stem] = (word,1)

	output = [wordcount + (root,) for root,wordcount in counts.items()]
	output.sort(key=lambda x: (-x[1],x[0]))
	return [tup[0] for tup in output[:n]]
	# for item in output:
	# 	print '%s:%d (Root: %s)' % item
