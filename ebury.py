from settings import *
from urllib3 import PoolManager
from uuid import uuid4
from base64 import b64encode
from urllib.parse import urlencode
import resources
import time
import json

class Ebury(PoolManager):
	def __init__(self, env):
		super(Ebury, self).__init__()
		self.load_settings(env)

		self.auth_request = self.request('GET',
			'%s/authenticate?scope=openid&response_type=code&'\
			'client_id=%s&state=%s&redirect_uri=%s' % (self.AUTH_URL, self.APP_CLIENT_ID, self.STATE, self.REDIRECT_URI)
		)
		time.sleep(1)		
		
		if self.auth_request.status == 200:
			print('\n### 1 ###\n/authenticate HTTP 200, sending login info\n###\n')
			self.login = self.urlopen('POST',
			    '%s/login' % self.AUTH_URL,
			    body = urlencode({
			        'client_id': self.APP_CLIENT_ID,
			        'state': self.STATE,
			        'email': self.EMAIL,
			        'password': self.PASS
			    }),
			    headers = {
			        'Content-Type': 'application/x-www-form-urlencoded',
			        'Authorization': 'Basic %s' % self.credentials
			    },
			   	redirect = False
			)
		else:
			print("Auth request did not return login form\n")
			return

		if self.login.status == 302:
			print('\n### 2 ###\n/login HTTP 302, grab code from redirect uri\n###\n')
			self.code = self.login.headers.get('Location').split('?')[1].split('&')[0].split('=')[1]
			print('### getting token ###\n')
			self.token = self.urlopen('POST',
	    		'%s/token' % self.AUTH_URL,
	    		body = urlencode({
	        		'grant_type': 'authorization_code',
	        		'code': self.code,
	        		'redirect_uri': self.REDIRECT_URI,
	        		'state': self.STATE
	    		}),
	    		headers = {
	        		'Content-Type': 'application/x-www-form-urlencoded',
	        		'Authorization': 'Basic %s' % self.credentials
	    		}
			)
			self.token_response = json.loads(self.token.data.decode('utf-8'))
			self.TOKEN = self.token_response['access_token']
		else:
			print("Login attemp did not return redirect with OAuth code\n")
			return

		self.headers = {
			'x-api-key': self.X_API_KEY,
			'Authorization': 'Bearer %s' % self.TOKEN,
			'X-CONTACT-ID': self.CONTACT_ID,
			'Content-Type': 'application/json'
    	}


	def load_settings(self, env):
		self.env = env
		if env in SETTINGS.keys():
			self.API_BASE = SETTINGS[env]['API_BASE']
			self.AUTH_URL = SETTINGS[env]['AUTH_URL']
			self.EMAIL = SETTINGS[env]['EMAIL']
			self.PASS = SETTINGS[env]['PASS']
			self.CLIENT_ID = SETTINGS[env]['CLIENT_ID']
			self.CONTACT_ID = SETTINGS[env]['CONTACT_ID']
			self.STATE = uuid4().hex
			self.REDIRECT_URI = SETTINGS[env]['REDIRECT_URI']
			self.X_API_KEY = SETTINGS[env]['X_API_KEY']
			self.APP_CLIENT_ID = SETTINGS[env]['APP_CLIENT_ID']
			self.CLIENT_SECRET = SETTINGS[env]['CLIENT_SECRET']
			self.credentials = b64encode(bytes('%s:%s' % (self.APP_CLIENT_ID, self.CLIENT_SECRET),
					'utf-8')).decode('utf-8')
			print('Settings for %s done' % env)
		else:
			print('Settings for %s environment not found' % env)

	def new(self, resource):
		if resource == 'quote':
			return resources.Quote(self)
		if resource == 'trade':
			return resources.Trade(self)
		if resource == 'beneficiary':
			return resources.Beneficiary(self)
		if resource == 'payment':
			return resources.Payment(self)

	def Quotes(self, quote_data, clientid=None):
		return resources.Quote(self, quote_data, clientid=clientid)

	def Trades(self, trade_data):
		return resources.Trade(self, trade_data, )

	def Beneficiary(self, bene_data):
		return resources.Beneficiary(self, bene_data)

	def Payments(self, pay_data):
		return resources.Payment(self, pay_data)

	def Multipayments(self, mpay_data, sell_currency, tradeId=None):
		return resources.Multipayment(self, mpay_data, sell_currency, tradeId=tradeId)
