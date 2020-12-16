from flask import Flask, request, render_template
from redis import Redis, RedisError, StrictRedis
import json
import random
import time

import pandas as pd
import numpy as np
import re
import string
import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle

from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram

REQUESTS = Counter('flask_redis_search_twitter_app_requests_total', 'How many times the application has been accessed')
EXCEPTIONS = Counter('flask_redis_search_twitter_app_exceptions_total', 'How many times the application issued an exception')

INPROGRESS = Gauge('flask_redis_search_twitter_app_inprogress_gauge', 'How many requests to the app are currently in progress')
LAST = Gauge('flask_redis_search_twitter_app_accessed_gauge', 'When was the application last accessed')

LATENCY = Summary('flask_redis_search_twitter_app_latency_seconds', 'time needed for a request')
LATENCY_HIS = Histogram('flask_redis_search_twitter_app_latency_histogram_seconds', 'time needed for a request', buckets=[0.01, 0.05, 0.1, 0.2,0.5,0.75, 1.0, 1.5, 2.0, 3.0])


app = Flask(__name__)

def preprocess_tweet(text):
	# Check characters to see if they are in punctuation
	nopunc = [char for char in text if char not in string.punctuation]
	# Join the characters again to form the string.
	nopunc = ''.join(nopunc)
	# convert text to lower-case
	nopunc = nopunc.lower()
	# remove pic 
	nopunc = re.sub(r'pic.twitter.com/[\w]*',"", nopunc)
	# remove URLs
	nopunc = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', nopunc)
	nopunc = re.sub(r'http\S+', '', nopunc)
	# remove special caracters
	nopunc = re.sub(r'\W+', ' ', nopunc)
	# remove usernames
	nopunc = re.sub('@[^\s]+', '', nopunc)
	# remove the # in #hashtag
	nopunc = re.sub(r'#([^\s]+)', r'\1', nopunc)
	#remove punctuation
	nopunc = re.sub(r'[^\w\s]','',nopunc)
	# remove words with only one character
	nopunc =  re.sub(r"\b[a-zA-Z]\b", "", nopunc)
	# remove repeated characters
	nopunc = word_tokenize(nopunc)
	# remove stopwords from final word list
	return [word for word in nopunc if word not in stopwords.words('english')]
"""
def clean_words(df):
	df_text = df.copy()
	df_text["clean_text"] = df_text["text"].apply(lambda x: preprocess_tweet([x]))
	return df_text

def tag_words(df):
	tag_words = [TaggedDocument(d, [i]) for i, d in enumerate(df.clean_text)]
	return tag_words
"""
def train_model():
	df = pd.read_csv("ML/tweets.csv", usecols=['text', 'id'])
	df_text = df.copy()
	df_text["clean_text"] = df_text["text"].apply(lambda x: preprocess_tweet([x]))

	tag_words = [TaggedDocument(d, [i]) for i, d in enumerate(df_text.clean_text)]

	modeldoc2vec = Doc2Vec(tag_words, vector_size=20, window=5, min_count=1, workers=-1, epochs = 20)

	#print('Storing model to redis...')

	pickle_model = pickle.dump(modeldoc2vec, open('ML/Doc2VecModelFinal.pkl','wb'))
	"""
	try:
		redis_client.set('doc2vecmodel', pickle_model)
	except RedisError as e:
		print('Storage model threw an error.')
		print(e)
	"""

def get_doc2vecmodel():
	#pickle_model = redis_client.get('doc2vecmodel')
	Doc2VecModelFinal = pickle.load(open('ML/Doc2VecModelFinal.pkl','rb'))
	return Doc2VecModelFinal

def get_similarities(model, sentence):
	try:
		example_result_model = model.docvecs.most_similar(positive=[model.infer_vector([sentence])], topn=20)
		return example_result_model
	except RedisError as e:
		print('Getting the result of the model threw an error.')
		print(e)

def get_tweet(df,model, sentence):
	resultsimilarity = get_similarities(model, sentence)
	tweet_similar = []
	for elem in resultsimilarity:
		tweet_similar.append({'id': elem[0],'tweets': df.text[elem[0]],'score': elem[1]})
	#print(tweet_similar)
	#return tweet_similar
	sent = tweet_similar
	INPROGRESS.dec()
	return render_template('index.html', result=sent)

def get_tweet_only(df, model, sentence):
	resultsimilarity = get_similarities(model, sentence)
	only_tweet_similar = []
	for elem in resultsimilarity:
		only_tweet_similar.append(df.text[elem[0]])
	#print(tweet_similar)
	sent = only_tweet_similar
	INPROGRESS.dec()
	return render_template('index.html', result=sent)


@app.route('/', methods=['GET', 'POST'])
def index():
	REQUESTS.inc()
	# Application will fail 0.1
	with EXCEPTIONS.count_exceptions():
		if random.random() < 0.1:
			raise Exception

	LAST.set(time.time())
	INPROGRESS.inc()
	start = time.time()
	time.sleep(random.random())

	df = pd.read_csv("ML/tweets.csv", usecols=['text', 'id'])
	model = get_doc2vecmodel()
	get_doc2vecmodel()

	if request.method == 'POST':
		sentence_form = request.form
		if sentence_form['form_type'] == 'get_tweets':
			return get_tweet_only(df, model, sentence_form['sentence']) 
	
	INPROGRESS.dec()
	lat = time.time()
	LATENCY.observe(lat - start)
	LATENCY_HIS.observe(lat - start)

	return render_template('index.html')

if __name__ == '__main__':
	start_http_server(8050)
	nltk.download('punkt')
	nltk.download('stopwords')
	redis_client = StrictRedis(host='redis', port=6379)
	app.run(host='0.0.0.0')

