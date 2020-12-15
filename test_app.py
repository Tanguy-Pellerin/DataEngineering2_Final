import unittest
import os
import requests

class FlaskTests(unittest.TestCase):
	
	def test_a_index(self):
		responce = requests.get('http://localhost:5000')
		self.assertEqual(responce.status_code, 200)
"""
	def setUp(self):
		os.environ['NO_PROXY'] = '0.0.0.0'
		self.user = {
			'uid': 314,
			'fname': "Joerge",
			"lname": "Carmen",
			"credit": 30
		}
		pass
		
	def tearDown(self):
		pass

	
	def test_a_index(self):
		responce = requests.get('http://localhost:5000')
		self.assertEqual(responce.status_code, 200)
		
	def test_b_add_user(self):
		
		params = {
			'uid': self.user['uid'],
			'fname': self.user['fname'],
			"lname": self.user['lname'],
			"form_type": "add_user"
		}
		responce = requests.post('http://localhost:5000', data=params)
		self.assertEqual(responce.status_code, 200)
		#self.assertEqual(responce.content, 'success'.encode())
		
	def test_c_add_credit(self):
		
		params = {
			'uid': self.user['uid'],
			'credit': self.user['credit'],
			"form_type": "add_credit"
		}
		responce = requests.post('http://localhost:5000', data=params)
		self.assertEqual(responce.status_code, 200)
		#self.assertEqual(responce.content, 'success'.encode())
	
	def test_d_view_user(self):
		params = {
			'uid': self.user['uid'],
			"form_type": "view_user"
		}
		expected = "first name: {}, last name: {}, credit: {}".format(
																self.user['fname'],
																self.user['lname'],
																float(self.user['credit'])
																)
		responce = requests.post('http://localhost:5000', data=params)
		self.assertEqual(responce.status_code, 200)
		#self.assertEqual(responce.content, expected.encode())
"""
if __name__ == '__main__':
	unittest.main()		


