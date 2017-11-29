# ebury-python
Python library for Ebury's API


A) Authentication and creating the api connection instance.

api = ebury.Ebury('LOCAL')

'LOCAL' is the environment as defined in the settings 

This instance can generate and return Ebury API resources 

1) Quotes

cota = {'trade_type': 'spot', 
    'buy_currency': 'EUR', 
    'amount': 10000.0, 
    'operation': 'buy', 
    'sell_currency': 'GBP',
}

>>> quote = api.Quotes(cota)

The Quotes object will print the http response data

>>> quote
{'book_trade': '/trades?client_id=EBPCLI00004&quote_id=db6906a59433d54e50987dd077161114', 'buy_amount': 10000.0, 'buy_currency': 'EUR', 'inverse_rate': 0.912068, 'quote_id': 'db6906a59433d54e50987dd077161114', 'quoted_rate': 1.09641, 'sell_amount': 9120.68, 'sell_currency': 'GBP', 'value_date': '2017-10-20'}

2) Trades




