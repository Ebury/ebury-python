import json
import pprint

class Entity(object):

	def validate_passed_data():
		pass

	#load passed atributes into self attributes
	def load_attributes():
		validate_passed_data():
		pass

	def __getattr__(self, attr):
		return json.loads(self._request.data.decode('utf-8'))[attr]

	def __repr__(self):
		return str(json.loads(self._request.data.decode('utf-8')))


class Quote(Entity):
	def __init__(self, api, quote_data=None):
		self._session = api
		self._request = None
		if isinstance(quote_data, dict):
			for key in quote_data:
				setattr(self, key, quote_data[key])
			self.post(quote_data)

	def post(self, data):
		self._request = self._session.urlopen('POST',
    		'%s/quotes?quote_type=quote&client_id=%s' 
    		% (self._session.API_BASE, self._session.CLIENT_ID),
    		body=json.dumps(data), headers=self._session.headers)
		return self._request.status


class Trade(Entity):
	def __init__(self, api, trade_data=None):
		self._session = api
		self._request = None
		self._defaultBody = {'reason': 'test', 'trade_type': 'spot'}
		if isinstance(trade_data, Quote):
			self.post(trade_data)

	def post(self, quote, tradeBody=None):
		if tradeBody is None:
			tradeBody = self._defaultBody

		self._request = self._session.urlopen('POST',
                '%s/trades?quote_id=%s&client_id=%s' 
                % (self._session.API_BASE, quote.quote_id, self._session.CLIENT_ID),
                body = json.dumps(tradeBody), headers=self._session.headers)
		return self._request.status

	def get(self, trade_id):
		self._request = self._session.urlopen('GET',
			'%s/trades/%s?client_id=%s'
			% (self._session.API_BASE, trade_id, self._session.CLIENT_ID),
			headers = self._session.headers)
		return self._request.status


class Beneficiary(Entity):
	def __init__(self, api, bene_data=None):
		self._session = api
		self._request = None
		if isinstance(bene_data, str):
			self.get(bene_data)
		elif isinstance(bene_data, dict):
			self.post(bene_data)

	def post(self, data):

		self._request = self._session.urlopen('POST', 
			'%s/beneficiaries?client_id=%s' 
                % (self._session.API_BASE, self._session.CLIENT_ID),
                body=json.dumps(data), headers=self._session.headers)
		return self._request.status

	def get(self, bene_id):

		self._request = self._session.urlopen('GET',
			'%s/beneficiaries/%s?client_id=%s' 
                % (self._session.API_BASE, bene_id, self._session.CLIENT_ID),
                headers=self._session.headers)
		return self._request.status



class Payment(Entity):
	def __init__(self, api, pay_data=None):
		self._session = api
		self._request = None
		if isinstance(pay_data, str):
			self.get(pay_data)

	def post(self, data):

		self._request = self._session.urlopen('POST',
			'%s/payments?client_id=%s' % 
			(self._session.API_BASE, self._session.CLIENT_ID),
			body = json.dumps(data), headers=self._session.headers)
		return self._request.status

	
	def get(self, pi):
		self._request = self._session.urlopen('GET',
			'%s/payments/%s?client_id=%s' % 
			(self._session.API_BASE, pi, self._session.CLIENT_ID),
			headers=self._session.headers)
		return	self._request.status

class Multipayment(Entity):
	def __init__(self, api, mpay_data=None):
		self._session = api
		self._request = None

