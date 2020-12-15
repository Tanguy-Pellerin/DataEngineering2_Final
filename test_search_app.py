import unittest
import os
import requests

class FlaskTests(unittest.TestCase):
	
	def test_a_index(self):
		responce = requests.get('http://localhost:5000')
		self.assertEqual(responce.status_code, 200)

if __name__ == '__main__':
	unittest.main()		


