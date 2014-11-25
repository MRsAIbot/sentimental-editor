from textblob import TextBlob
import numpy as np

# text = '''
# The titular threat of The Blob has always struck me as the ultimate movie
# monster: an insatiably hungry, amoeba-like mass able to penetrate
# virtually any safeguard, capable of--as a doomed doctor chillingly
# describes it--"assimilating flesh on contact.
# Snide comparisons to gelatin be damned, it's a concept with the most
# devastating of potential consequences, not unlike the grey goo scenario
# proposed by technological theorists fearful of
# artificial intelligence run rampant.
# '''
text = '''
Biggest congratulations to @TbirdFilms for The Riot Club. One of my favorite films of the year! I've never been so pleasantly disturbed...
'''

# blob = TextBlob(text)
# blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
#                     #  ('threat', 'NN'), ('of', 'IN'), ...]

# blob.noun_phrases   # WordList(['titular threat', 'blob',
#                     #            'ultimate movie monster',
#                     #            'amoeba-like mass', ...])

# sentence_polarities = []

# for sentence in blob.sentences:
# 	sentence_polarities.append(sentence.sentiment.polarity)
# 	# print(sentence.sentiment.polarity)
# # 0.060
# # -0.341

# q = np.median(sentence_polarities)
# print q

# print int(round(translate_result(q)))

def translate_result(x):
	return (x+1)*5

def classify_sentiment(tweet):
	blob = TextBlob(tweet)
	sentence_polarities = []
	for sentence in blob.sentences:
		sentence_polarities.append(sentence.sentiment.polarity)
	median = np.median(sentence_polarities)
	return int(round(translate_result(median)))

print classify_sentiment(text)