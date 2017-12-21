import json
import pprint

class Entity(object):

	def validate(self, passed_data):
		pass

	#load passed atributes into self attributes
	def load_attributes(self, passed_data):
		self.validate(passed_data)
		for key in passed_data:
			setattr(self, key, passed_data[key])

	def __getattr__(self, attr):
		return json.loads(self._request.data.decode('utf-8'))[attr]

	def __repr__(self):
		return str(json.loads(self._request.data.decode('utf-8')))


class Quote(Entity):
	def __init__(self, api, quote_data=None, clientid=None):
		self._session = api
		self._request = None
		if clientid is None:
			self._clientid = self._session.CLIENT_ID
		else:
			self._clientid = clientid
		if isinstance(quote_data, dict):
			self.load_attributes(quote_data)
			self.post(quote_data)

	def post(self, data):
		self._request = self._session.urlopen('POST',
    		'%s/quotes?quote_type=quote&client_id=%s' 
    		% (self._session.API_BASE, self._clientid),
    		body=json.dumps(data), headers=self._session.headers)
		return self._request.status


class Trade(Entity):
	def __init__(self, api, trade_data=None):
		self._session = api
		self._request = None
		self._defaultBody = {'reason': 'test', 'trade_type': 'spot'}
		if isinstance(trade_data, Quote):
			self.post(trade_data)
		elif isinstance(trade_data, str):
			self.get(trade_data)

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
	def __init__(self, api, pay_data=None, trade=None, bene=None):
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
	def __init__(self, api, mpay_data=None, sell_currency=None, tradeId=None):
		self._session = api
		self._request = None
		if sell_currency:
			self.url = '%s/multipayments?client_id=%s&accept_immediately=true&sell_currency=%s' % (self._session.API_BASE, self._session.CLIENT_ID, sell_currency)
		elif tradeId:
			self.url = '%s/multipayments?client_id=%s&accept_immediately=true&trade_id=%s' % (self._session.API_BASE, self._session.CLIENT_ID, tradeId)
		else:
			self.url = '%s/multipayments?client_id=%s&accept_immediately=true' % (self._session.API_BASE, self._session.CLIENT_ID)
		self.post(mpay_data)

	
	def post(self, data):

		self._request = self._session.urlopen('POST',
			self.url,
			body = json.dumps(data), headers=self._session.headers)
		return self._request.status

class Metada(Entity):
	pass 


