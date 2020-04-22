# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/9 20:28

@desc:

'''

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import NetworkError
from ccxt.base.errors import NotSupported
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import RequestTimeout
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadSymbol
from requests.exceptions import HTTPError, Timeout, TooManyRedirects, RequestException
import math
from ssl import SSLError
import hashlib


class zg(Exchange):
    def describe(self):
        return self.deep_extend(super(zg, self).describe(), {
            'id': 'zg',
            'name': 'zg',
            'countries': ['CN'],  # Seychelles
            'version': 'v1',
            'userAgent': None,
            'rateLimit': 2000,
            'has': {
                'CORS': False,
                'fetchOHLCV': True,
                'withdraw': True,
                'editOrder': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'fetchMyTrades': True,
                'fetchLedger': True,
                'fetchTransactions': 'emulated',
            },
            # 1min,5min,15min,30min,hour,day,week
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1d',
                '1w': '1w',
                '1M': '1M'
            },
            'urls': {
                'logo': 'data:image/png;base64,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',
                # 'api': 'https://api.zg.com/openapi',
                'api': 'https://api.zgnext.com/openapi',
                'www': 'https://www.zg.com/',
                'doc': 'https://github.com/zgcom/OpenAPI/blob/master/REST%20API%20CN.md',
                'fees': '',
                'referral': '',
            },
            'api': {
                'public': {
                    'get': [
                        'tickers',
                        'depth',
                        'trades',
                        'klines',
                        'brokerInfo'
                    ],
                },
                'private': {
                    'post': [
                        'order',  # 创建新订单
                        'order/test',  # 测试创建订单
                    ],
                    'get': [
                        'account ',  # 获取用户资产
                        'order',  # 查询订单
                        'openOrders',  # 当前订单
                        'historyOrders',  # 历史订单
                    ],
                    'delete': [
                        'order',  # 删除订单
                    ]
                },
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetBrokerInfo()
        result = []
        for market in response['symbols']:
            id = market['symbol']
            base = market['baseAsset']
            quote = market['quoteAsset']
            symbol = base + '/' + quote
            active = True if market['status'] == 'trading' else False
            filters = {}
            for iterm in market['filters']:
                for key in iterm.keys():
                    filters[key] = iterm[key]
            precision = {
                'amount': self.safe_integer(filters, 'stepSize'),
                'price': self.safe_integer(filters, 'tickSize')
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'baseId': base,
                'quote': quote,
                'quoteId': quote,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': self.safe_integer(filters, 'minQty'),
                        'max': self.safe_integer(filters, 'maxQty'),
                    },
                    'price': {
                        'min': self.safe_integer(filters, 'minPrice'),
                        'max': self.safe_integer(filters, 'maxPrice'),
                    },
                    'cost': {
                        'min': 0,
                        'max': None,
                    },
                },
                'info': market
            })
        return result

    # def fetch_tickers(self, symbols=None, params={}):
    #     self.load_markets()
    #     response = self.publicGetTickers()
    #     result = {}
    #     for ticker in response['ticker']:
    #         data = self.parse_ticker(ticker, self.safe_integer(response, 'timestamp'))
    #         symbol = self.safe_string(ticker, 'symbol')
    #         if symbol:
    #             result[symbol] = data
    #     return result
    #
    # def fetch_ticker(self, symbol, params={}):
    #     self.load_markets()
    #     market = self.market(symbol)
    #     if not market['active']:
    #         raise ExchangeError(self.id + ': symbol ' + symbol + ' is delisted')
    #     tickers = self.fetch_tickers()
    #     ticker = self.safe_value(tickers, market['id'])
    #     if ticker is None:
    #         raise ExchangeError(self.id + ' ticker symbol ' + symbol + ' not found')
    #     return ticker
    #
    # def parse_ticker(self, ticker, timestamp):
    #     return {
    #         'symbol': ticker['symbol'],
    #         'timestamp': timestamp,
    #         'high': self.safe_float(ticker, 'high'),
    #         'low': self.safe_float(ticker, 'low'),
    #         'bid': self.safe_float(ticker, 'buy'),
    #         'ask': self.safe_float(ticker, 'sell'),
    #         'last': self.safe_float(ticker, 'last'),
    #         'change': self.safe_float(ticker, 'change'),
    #         'vol': self.safe_float(ticker, 'vol'),
    #         'info': ticker
    #     }

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 500
        request = {
            'symbol': market['id'],
            'interval': self.timeframes[timeframe],
            'limit': limit
        }
        response = self.publicGetKlines(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 500
        request = {
            'symbol': market['id'],
            'limit': limit
        }
        response = self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if limit is None:
            limit = 500
        request = {
            'symbol': market['id'],
            'limit': limit
        }
        response = self.publicGetTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'time')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'qty')
        cost = price * amount
        return {
            'info': trade,
            'id': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': self.safe_string(market, 'symbol'),
            'type': None,
            'side': self.safe_string(trade, 'side'),
            'order': None,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetAccount(params)
        balances = self.safe_value(response, 'result')
        if balances is None:
            raise ExchangeError(self.id + ' fetch balance error: ' + response['message'])
        result = {'info': response}
        for key in balances.keys():
            b = balances[key]
            account = self.account()
            account['free'] = self.safe_float(b, 'available')
            account['used'] = self.safe_float(b, 'freeze') + self.safe_float(b, 'other_freeze')
            code = self.safe_currency_code(key)
            result[code] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'side': side.upper(),
            'quantity': str(amount),
            'type': type.upper()
        }
        if type == 'limit':
            request['price'] = price
        order_info = self.privatePostOrder(self.extend(request, params))
        return self.parse_order(order_info, market)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        timestamp = self.safe_float(order, 'ctime')
        timestamp = int(timestamp * 1000)
        price_ = self.safe_float(order, 'price')
        deal_fee = self.safe_float(order, 'deal_fee')
        marker_fee = self.safe_float(order, 'maker_fee')
        taker_fee = self.safe_float(order, 'taker_fee')
        fee = deal_fee + marker_fee + taker_fee
        remaining = self.safe_float(order, 'left')
        amount = self.safe_float(order, 'amount')
        filled = amount - remaining
        side = self.safe_integer(order, 'side')
        side_ = 'sell' if side == 1 else 'buy'
        type = self.safe_integer(order, 'type')
        type = 'limit' if type == 1 else 'market'
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'status': None,
            'symbol': market['symbol'],
            'type': type,
            'side': side_,
            'price': price_,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'cost': None,
            'trades': None,
            'fee': fee,
        }

    def cancel_order(self, id, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.privatePostTradeCancel({'order_id': id, 'market': market['id']})
        code = self.safe_integer(response, 'code')
        message = self.safe_string(response, 'message')
        if code != 0:
            raise ExchangeError(self.id + ' cancel order error: ' + message)

        result = self.safe_value(response, 'result')
        if result is None:
            raise ExchangeError(self.id + ' cancel order error: ' + response['message'])
        return self.extend(self.parse_order(result, market), {
            'id': id,
            'status': 'canceled',
        })

    def fetch_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'order_id': id,
            'offset': 0,
            'limit': 20
        }
        response = self.privatePostOrderDeals(self.extend(request, params))
        code = self.safe_integer(response, 'code')
        message = self.safe_string(response, 'message')
        if code != 0:
            raise ExchangeError(self.id + ' fetch order error: ' + message)

        result = self.safe_value(response, 'result')
        if result is None:
            raise ExchangeError(self.id + ' fetch order error: ' + response['message'])
        return result

    def fetch_open_orders(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        limit = 20 if limit is None else limit
        params['offset'] = 0 if 'offset' not in params else params['offset']
        request = {
            'market': market['id'],
            'limit': limit,
        }
        response = self.privatePostOrderPending(self.extend(request, params))
        code = self.safe_integer(response, 'code')
        message = self.safe_string(response, 'message')
        if code != 0:
            raise ExchangeError(self.id + ' fetch open orders error: ' + message)

        result = self.safe_value(response, 'result')
        if result is None:
            raise ExchangeError(self.id + ' fetch open orders error: ' + response['message'])
        records = self.safe_value(result, 'records')
        records = records if records else []
        return self.parse_orders(records, market)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        limit = 20 if limit is None else limit
        params['offset'] = 0 if 'offset' not in params else params['offset']
        request = {
            'market': market['id'],
            'limit': limit
        }
        response = self.privatePostOrderFinished(self.extend(request, params))
        code = self.safe_integer(response, 'code')
        message = self.safe_string(response, 'message')
        if code != 0:
            raise ExchangeError(self.id + ' fetch close orders error: ' + message)

        result = self.safe_value(response, 'result')
        if result is None:
            raise ExchangeError(self.id + ' fetch close orders error: ' + response['message'])
        records = self.safe_value(result, 'records')
        records = records if records else []
        return self.parse_orders(records, market)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        query = '/' + path
        if api == 'public':
            if query == '/brokerInfo':
                url = self.urls['api'] + '/' + self.version + query
            else:
                url = self.urls['api'] + '/quote/' + self.version + query
            if params:
                url += '?' + self.urlencode(params)
        else:
            url = self.urls['api'] + '/' + self.version + query
            headers = {
                'X-BH-APIKEY': self.apiKey
            }
            body = self.keysort(params)
            signature = self.hmac(self.encode(query), self.encode(self.secret))
            body['signature'] = signature
        return {'url': url, 'method': method, 'body': body, 'headers': headers}


if __name__ == '__main__':
    exapi = zg({
        # 'apiKey': '0cf34f75f336418088636adc15323a13',
        # 'secret': 'a5fcfa992afa4bed9ac0638fc1b79288',
        'apiKey': 'tAQfOrPIZAhym0qHISRt8EFvxPemdBm5j5WMlkm3Ke9aFp0EGWC2CGM8GHV4kCYW',
        'secret': 'lH3ELTNiFxCQTmi9pPcWWikhsjO04Yoqw3euoHUuOLC3GYBW64ZqzQsiOEHXQS76',
        'enableRateLimit': False,
        'timeout': 20000,
        # 'proxies': {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    })
    # print(exapi.fetch_markets())
    # print(exapi.fetch_order_book("ADA/BTC"))
    # print(exapi.fetch_ohlcv("ADA/BTC"))
    # print(exapi.fetch_balance())
    print(exapi.create_order('ETH/BTC', 'limit', 'buy', 1, 0.1, params={'recvWindow': 5000,
                                                                        'timestamp': 1538323200000}))

