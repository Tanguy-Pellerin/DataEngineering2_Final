from flask import Flask, request, render_template
from redis import Redis, RedisError, StrictRedis
import json
import random
import time
import pandas as pd
import numpy as np
import preprocessor as p
from gensim.models import FastText
import nltk
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
LATENCY_HIS = Histogram('flask_redis_search_twitter_app_latency_histogram_seconds', 'time needed for a request', buckets=[0.0001, 0.001, 0.01, 0.1, 1.0, 1.5, 2.0, 3.0])


app = Flask(__name__)

	

@app.route('/', methods=['GET', 'POST'])
def index():
	REQUESTS.inc()
	
	# Application will fail 0.1
	#with EXCEPTIONS.count_exceptions():
		#if random.random() < 0.1:
			#raise Exception

	LAST.set(time.time())
	INPROGRESS.inc()
	start = time.time()
	time.sleep(random.random())



	INPROGRESS.dec()
	lat = time.time()
	LATENCY.observe(lat - start)
	LATENCY_HIS.observe(lat - start)

	return render_template('index.html')

if __name__ == '__main__':
	start_http_server(8010)
	redis_client = StrictRedis(host='redis', port=6379)
	app.run(host='0.0.0.0')
	
	
	
	
