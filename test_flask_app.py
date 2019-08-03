import unittest
from flask import *
from flask_app import app
from mock import Mock
from flask_app import *

class TestCase(unittest.TestCase):

    def test_inboundApi(self):
    	credentials = {"authentication": {"username": "azr3","password": "9LLV6I4ZWI"},"from": "441235330053","to": "441224980093","text": "STOP"}
    	with app.test_client() as client:
    		rv = client.post('inbound/sms',data = json.dumps(credentials), content_type='application/json')
    	self.assertEqual(rv.status_code, 200)

    def test_outboundApi(self):
    	credentials = {"authentication": {"username": "azr3","password": "9LLV6I4ZWI"},"from": "441235330053","to": "441224980093","text": "STOP"}
    	with app.test_client() as client:
    		rv = client.post('outbound/sms',data = json.dumps(credentials), content_type='application/json')
    	self.assertEqual(rv.status_code, 200)

    def test_validation(self):
    	test = validation ("23456784567","2334567234567","test")
    	self.assertEqual("valid", test )

if __name__ == '__main__':
	unittest.main()