import unittest
import os
import requests
import time

class FlaskTests(unittest.TestCase):
	
	def test_a_index(self):
		responce = requests.get('http://0.0.0.0:8050/')
		self.assertEqual(responce.status_code, 200)
		
	def test_b_get_tweet(self):
		parameters = {
			'sentence': 'The media and establishment want me out of the race so badly -  I WILL NEVER DROP OUT OF THE RACE, WILL NEVER LET MY SUPPORTERS DOWN! #MAGA',
			'form_type': 'get_tweets'
		}
		responce = requests.post('http://0.0.0.0:8050/', data=parameters)
		self.assertEqual(responce.status_code, 200)

if __name__ == '__main__':
	time.sleep(1)
	unittest.main()		


