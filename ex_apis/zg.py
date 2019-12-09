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
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable

class zg(Exchange):
    def describe(self):
        return self.deep_extend(super(zg, self).describe(), {
            'id': 'zg',
            'name': 'zg',
            'countries': ['CN'],  # Seychelles
            'version': 'v0.0.6',
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
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '1h': '1h',
                '1d': '1d',
            },
            'urls': {
                'logo': 'data:image/png;base64,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',
                'api': 'https://api1.zg.com',
                'www': 'https://www.zg.com/',
                'doc': 'https://github.com/zgcom/API_Docs/wiki',
                'fees': '',
                'referral': '',
            },
            'api': {
                'public': {
                    'get': [

                    ],
                },
                'private': {
                    'get': [

                    ],
                    'post': [

                    ]
                },
            },
        })