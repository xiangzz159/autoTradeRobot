# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/9 20:28

@desc:

'''

from ccxt.base.exchange import Exchange
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import ROUND
from ccxt.base.decimal_to_precision import TRUNCATE


class zg(Exchange):
    def describe(self):
        return self.deep_extend(super(zg, self).describe(), {
            'id': 'zg',
            'name': 'zg',
            'countries': ['CN'],  # Seychelles
            'version': 'v1',
            'rateLimit': 500,
            'certified': True,
            'pro': True,
            # new metainfo interface
            'has': {
                'fetchDepositAddress': True,
                'CORS': False,
                'fetchBidsAsks': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchOHLCV': True,
                'fetchMyTrades': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchClosedOrders': 'emulated',
                'withdraw': True,
                'fetchFundingFees': True,
                'fetchDeposits': True,
                'fetchWithdrawals': True,
                'fetchTransactions': False,
                'fetchTradingFee': True,
                'fetchTradingFees': True,
            },
            'timeframes': {
                '1m': '1m',
                '3m': '3m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '8h': '8h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '1M': '1M',
            },
            'urls': {
                'logo': 'data:image/png;base64,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',
                # 'api': 'https://api.zg.com/openapi',
                'api': {
                     'public': 'https://api.zg8.com/openapi',
                    'private': 'https://api.zg8.com/openapi'
                },
                'www': 'https://www.zg.com/',
                'doc': 'https://github.com/zgcom/OpenAPI/blob/master/REST%20API%20CN.md',
                'fees': '',
                'referral': '',
            },
            'api': {
                'web': {
                    'get': [
                        'exchange/public/product',
                        'assetWithdraw/getAllAsset.html',
                    ],
                },
                # the API structure below will need 3-layer apidefs
                'sapi': {
                    'get': [
                        'accountSnapshot',
                        # these endpoints require self.apiKey
                        'margin/asset',
                        'margin/pair',
                        'margin/allAssets',
                        'margin/allPairs',
                        'margin/priceIndex',
                        # these endpoints require self.apiKey + self.secret
                        'asset/assetDividend',
                        'margin/loan',
                        'margin/repay',
                        'margin/account',
                        'margin/transfer',
                        'margin/interestHistory',
                        'margin/forceLiquidationRec',
                        'margin/order',
                        'margin/openOrders',
                        'margin/allOrders',
                        'margin/myTrades',
                        'margin/maxBorrowable',
                        'margin/maxTransferable',
                        'futures/transfer',
                        # https://binance-docs.github.io/apidocs/spot/en/#withdraw-sapi
                        'capital/config/getall',  # get networks for withdrawing USDT ERC20 vs USDT Omni
                        'capital/deposit/address',
                        'capital/deposit/hisrec',
                        'capital/deposit/subAddress',
                        'capital/deposit/subHisrec',
                        'capital/withdraw/history',
                        'sub-account/futures/account',
                        'sub-account/futures/accountSummary',
                        'sub-account/futures/positionRisk',
                        'sub-account/margin/account',
                        'sub-account/margin/accountSummary',
                        'sub-account/status',
                        # lending endpoints
                        'lending/daily/product/list',
                        'lending/daily/userLeftQuota',
                        'lending/daily/userRedemptionQuota',
                        'lending/daily/token/position',
                        'lending/union/account',
                        'lending/union/purchaseRecord',
                        'lending/union/redemptionRecord',
                        'lending/union/interestHistory',
                    ],
                    'post': [
                        'asset/dust',
                        'account/disableFastWithdrawSwitch',
                        'account/enableFastWithdrawSwitch',
                        'capital/withdraw/apply',
                        'margin/transfer',
                        'margin/loan',
                        'margin/repay',
                        'margin/order',
                        'sub-account/margin/enable',
                        'sub-account/margin/enable',
                        'sub-account/futures/enable',
                        'userDataStream',
                        'futures/transfer',
                        # lending
                        'lending/daily/purchase',
                        'lending/daily/redeem',
                    ],
                    'put': [
                        'userDataStream',
                    ],
                    'delete': [
                        'margin/order',
                        'userDataStream',
                    ],
                },
                'wapi': {
                    'post': [
                        'withdraw',
                        'sub-account/transfer',
                    ],
                    'get': [
                        'depositHistory',
                        'withdrawHistory',
                        'depositAddress',
                        'accountStatus',
                        'systemStatus',
                        'apiTradingStatus',
                        'userAssetDribbletLog',
                        'tradeFee',
                        'assetDetail',
                        'sub-account/list',
                        'sub-account/transfer/history',
                        'sub-account/assets',
                    ],
                },
                'fapiPublic': {
                    'get': [
                        'ping',
                        'time',
                        'brokerInfo',
                        'depth',
                        'trades',
                        'historicalTrades',
                        'aggTrades',
                        'klines',
                        'fundingRate',
                        'premiumIndex',
                        'ticker/24hr',
                        'ticker/price',
                        'ticker/bookTicker',
                        'allForceOrders',
                        'openInterest',
                        'leverageBracket',
                    ],
                },
                'fapiPrivate': {
                    'get': [
                        'allOrders',
                        'openOrder',
                        'openOrders',
                        'order',
                        'account',
                        'balance',
                        'positionMargin/history',
                        'positionRisk',
                        'userTrades',
                        'income',
                    ],
                    'post': [
                        'batchOrders',
                        'positionSide/dual',
                        'positionMargin',
                        'marginType',
                        'order',
                        'leverage',
                        'listenKey',
                    ],
                    'put': [
                        'listenKey',
                    ],
                    'delete': [
                        'batchOrders',
                        'order',
                        'allOpenOrders',
                        'listenKey',
                    ],
                },
                'v3': {
                    'get': [
                        'ticker/price',
                        'ticker/bookTicker',
                    ],
                },
                'public': {
                    'get': [
                        'ping',
                        'time',
                        'depth',
                        'trades',
                        'aggTrades',
                        'historicalTrades',
                        'klines',
                        'ticker/24hr',
                        'ticker/price',
                        'ticker/bookTicker',
                        'brokerInfo',
                    ],
                    'put': ['userDataStream'],
                    'post': ['userDataStream'],
                    'delete': ['userDataStream'],
                },
                'private': {
                    'get': [
                        'allOrderList',  # oco
                        'openOrderList',  # oco
                        'orderList',  # oco
                        'order',
                        'openOrders',
                        'allOrders',
                        'account',
                        'myTrades',
                    ],
                    'post': [
                        'order/oco',
                        'order',
                        'order/test',
                    ],
                    'delete': [
                        'orderList',  # oco
                        'order',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.001,
                    'maker': 0.001,
                },
            },
            'commonCurrencies': {
                'BCC': 'BCC',  # kept for backward-compatibility https://github.com/ccxt/ccxt/issues/4848
                'YOYO': 'YOYOW',
            },
            # exchange-specific options
            'options': {
                'fetchTradesMethod': 'publicGetTrades',  # publicGetTrades, publicGetHistoricalTrades
                'fetchTickersMethod': 'publicGetTicker24hr',
                'defaultTimeInForce': 'GTC',  # 'GTC' = Good To Cancel(default), 'IOC' = Immediate Or Cancel
                'defaultLimitOrderType': 'limit',  # or 'limit_maker'
                'defaultType': 'spot',  # 'spot', 'future'
                'hasAlreadyAuthenticatedSuccessfully': False,
                'warnOnFetchOpenOrdersWithoutSymbol': True,
                'recvWindow': 5 * 1000,  # 5 sec, binance default
                'timeDifference': 0,  # the difference between system clock and Binance clock
                'adjustForTimeDifference': False,  # controls the adjustment logic upon instantiation
                'parseOrderToPrecision': False,  # force amounts and costs in parseOrder to precision
                'newOrderRespType': {
                    'market': 'FULL',  # 'ACK' for order id, 'RESULT' for full order or 'FULL' for order with fills
                    'limit': 'RESULT',  # we change it from 'ACK' by default to 'RESULT'
                },
            },
            'exceptions': {
                'API key does not exist': AuthenticationError,
                'Order would trigger immediately.': InvalidOrder,
                'Account has insufficient balance for requested action.': InsufficientFunds,
                'Rest API trading is not enabled.': ExchangeNotAvailable,
                "You don't have permission.": PermissionDenied,  # {"msg":"You don't have permission.","success":false}
                'Market is closed.': ExchangeNotAvailable,  # {"code":-1013,"msg":"Market is closed."}
                '-1000': ExchangeNotAvailable,
                # {"code":-1000,"msg":"An unknown error occured while processing the request."}
                '-1003': RateLimitExceeded,
                # {"code":-1003,"msg":"Too much request weight used, current limit is 1200 request weight per 1 MINUTE. Please use the websocket for live updates to avoid polling the API."}
                '-1013': InvalidOrder,  # createOrder -> 'invalid quantity'/'invalid price'/MIN_NOTIONAL
                '-1021': InvalidNonce,  # 'your time is ahead of server'
                '-1022': AuthenticationError,  # {"code":-1022,"msg":"Signature for self request is not valid."}
                '-1100': InvalidOrder,  # createOrder(symbol, 1, asdf) -> 'Illegal characters found in parameter 'price'
                '-1104': ExchangeError,  # Not all sent parameters were read, read 8 parameters but was sent 9
                '-1128': ExchangeError,  # {"code":-1128,"msg":"Combination of optional parameters invalid."}
                '-2010': ExchangeError,
                # generic error code for createOrder -> 'Account has insufficient balance for requested action.', {"code":-2010,"msg":"Rest API trading is not enabled."}, etc...
                '-2011': OrderNotFound,  # cancelOrder(1, 'BTC/USDT') -> 'UNKNOWN_ORDER'
                '-2013': OrderNotFound,  # fetchOrder(1, 'BTC/USDT') -> 'Order does not exist'
                '-2014': AuthenticationError,  # {"code":-2014, "msg": "API-key format invalid."}
                '-2015': AuthenticationError,  # "Invalid API-key, IP, or permissions for action."
            },
        })

    def nonce(self):
        return self.milliseconds() - self.options['timeDifference']

    def fetch_time(self, params={}):
        type = self.safe_string_2(self.options, 'fetchTime', 'defaultType', 'spot')
        method = 'publicGetTime' if (type == 'spot') else 'fapiPublicGetTime'
        response = getattr(self, method)(params)
        return self.safe_integer(response, 'serverTime')

    def load_time_difference(self):
        serverTime = self.fetch_time()
        after = self.milliseconds()
        self.options['timeDifference'] = after - serverTime
        return self.options['timeDifference']

    def fetch_markets(self, params={}):
        defaultType = self.safe_string_2(self.options, 'fetchMarkets', 'defaultType', 'spot')
        type = self.safe_string(params, 'type', defaultType)
        query = self.omit(params, 'type')
        method = 'publicGetBrokerInfo' if (type == 'spot') else 'fapiPublicGetBrokerInfo'
        response = self.publicGetBrokerInfo()
        markets = self.safe_value(response, 'symbols')
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            future = ('maintMarginPercent' in market)
            spot = not future
            marketType = 'spot' if spot else 'future'
            id = self.safe_string(market, 'symbol')
            lowercaseId = self.safe_string_lower(market, 'symbol')
            baseId = market['baseAsset']
            quoteId = market['quoteAsset']
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            symbol = base + '/' + quote
            filters = self.index_by(market['filters'], 'filterType')
            precision = {
                'base': market['baseAssetPrecision'],
                'quote': market['quotePrecision'],
                'amount': self.safe_float(market, 'baseAssetPrecision'),
                'price': self.safe_float(market, 'quotePrecision'),
            }
            status = self.safe_string(market, 'status')
            active = (status == 'TRADING')
            entry = {
                'id': id,
                'lowercaseId': lowercaseId,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'type': marketType,
                'spot': spot,
                'future': future,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': math.pow(10, -precision['amount']),
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': -1 * math.log10(precision['amount']),
                        'max': None,
                    },
                },
            }
            if 'PRICE_FILTER' in filters:
                filter = filters['PRICE_FILTER']
                # PRICE_FILTER reports zero values for maxPrice
                # since they updated filter types in November 2018
                # https://github.com/ccxt/ccxt/issues/4286
                # therefore limits['price']['max'] doesn't have any meaningful value except None
                entry['limits']['price'] = {
                    'min': self.safe_float(filter, 'minPrice'),
                    'max': None,
                }
                maxPrice = self.safe_float(filter, 'maxPrice')
                if (maxPrice is not None) and (maxPrice > 0):
                    entry['limits']['price']['max'] = maxPrice
                entry['precision']['price'] = self.precision_from_string(filter['tickSize'])
            if 'LOT_SIZE' in filters:
                filter = self.safe_value(filters, 'LOT_SIZE', {})
                stepSize = self.safe_string(filter, 'stepSize')
                entry['precision']['amount'] = self.precision_from_string(stepSize)
                entry['limits']['amount'] = {
                    'min': self.safe_float(filter, 'minQty'),
                    'max': self.safe_float(filter, 'maxQty'),
                }
            if 'MARKET_LOT_SIZE' in filters:
                filter = self.safe_value(filters, 'MARKET_LOT_SIZE', {})
                entry['limits']['market'] = {
                    'min': self.safe_float(filter, 'minQty'),
                    'max': self.safe_float(filter, 'maxQty'),
                }
            if 'MIN_NOTIONAL' in filters:
                entry['limits']['cost']['min'] = self.safe_float(filters['MIN_NOTIONAL'], 'minNotional')
            result.append(entry)
        return result

    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        market = self.markets[symbol]
        key = 'quote'
        rate = market[takerOrMaker]
        cost = amount * rate
        precision = market['precision']['price']
        if side == 'sell':
            cost *= price
        else:
            key = 'base'
            precision = market['precision']['amount']
        cost = self.decimal_to_precision(cost, ROUND, precision, self.precisionMode)
        return {
            'type': takerOrMaker,
            'currency': market[key],
            'rate': rate,
            'cost': float(cost),
        }

    def fetch_balance(self, params={}):
        self.load_markets()
        defaultType = self.safe_string_2(self.options, 'fetchBalance', 'defaultType', 'spot')
        type = self.safe_string(params, 'type', defaultType)
        method = 'privateGetAccount' if (type == 'spot') else 'fapiPrivateGetAccount'
        query = self.omit(params, 'type')
        response = getattr(self, method)(query)
        #
        # spot
        #
        #     {
        #         makerCommission: 10,
        #         takerCommission: 10,
        #         buyerCommission: 0,
        #         sellerCommission: 0,
        #         canTrade: True,
        #         canWithdraw: True,
        #         canDeposit: True,
        #         updateTime: 1575357359602,
        #         accountType: "MARGIN",
        #         balances: [
        #             {asset: "BTC", free: "0.00219821", locked: "0.00000000"  },
        #         ]
        #     }
        #
        # futures(fapi)
        #
        #     {
        #         "feeTier":0,
        #         "canTrade":true,
        #         "canDeposit":true,
        #         "canWithdraw":true,
        #         "updateTime":0,
        #         "totalInitialMargin":"0.00000000",
        #         "totalMaintMargin":"0.00000000",
        #         "totalWalletBalance":"4.54000000",
        #         "totalUnrealizedProfit":"0.00000000",
        #         "totalMarginBalance":"4.54000000",
        #         "totalPositionInitialMargin":"0.00000000",
        #         "totalOpenOrderInitialMargin":"0.00000000",
        #         "maxWithdrawAmount":"4.54000000",
        #         "assets":[
        #             {
        #                 "asset":"USDT",
        #                 "walletBalance":"4.54000000",
        #                 "unrealizedProfit":"0.00000000",
        #                 "marginBalance":"4.54000000",
        #                 "maintMargin":"0.00000000",
        #                 "initialMargin":"0.00000000",
        #                 "positionInitialMargin":"0.00000000",
        #                 "openOrderInitialMargin":"0.00000000",
        #                 "maxWithdrawAmount":"4.54000000"
        #             }
        #         ],
        #         "positions":[
        #             {
        #                 "symbol":"BTCUSDT",
        #                 "initialMargin":"0.00000",
        #                 "maintMargin":"0.00000",
        #                 "unrealizedProfit":"0.00000000",
        #                 "positionInitialMargin":"0.00000",
        #                 "openOrderInitialMargin":"0.00000"
        #             }
        #         ]
        #     }
        #
        result = {'info': response}
        if type == 'spot':
            balances = self.safe_value(response, 'balances', [])
            for i in range(0, len(balances)):
                balance = balances[i]
                currencyId = self.safe_string(balance, 'asset')
                code = self.safe_currency_code(currencyId)
                account = self.account()
                account['free'] = self.safe_float(balance, 'free')
                account['used'] = self.safe_float(balance, 'locked')
                result[code] = account
        else:
            balances = self.safe_value(response, 'assets', [])
            for i in range(0, len(balances)):
                balance = balances[i]
                currencyId = self.safe_string(balance, 'asset')
                code = self.safe_currency_code(currencyId)
                account = self.account()
                account['used'] = self.safe_float(balance, 'initialMargin')
                account['total'] = self.safe_float(balance, 'marginBalance')
                result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=500, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'limit': limit
        }
        method = 'publicGetDepth' if market['spot'] else 'fapiPublicGetDepth'
        response = getattr(self, method)(self.extend(request, params))
        orderbook = self.parse_order_book(response)
        orderbook['nonce'] = self.safe_integer(response, 'lastUpdateId')
        return orderbook

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_integer(ticker, 'closeTime')
        symbol = None
        marketId = self.safe_string(ticker, 'symbol')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'lastPrice')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'highPrice'),
            'low': self.safe_float(ticker, 'lowPrice'),
            'bid': self.safe_float(ticker, 'bidPrice'),
            'bidVolume': self.safe_float(ticker, 'bidQty'),
            'ask': self.safe_float(ticker, 'askPrice'),
            'askVolume': self.safe_float(ticker, 'askQty'),
            'vwap': self.safe_float(ticker, 'weightedAvgPrice'),
            'open': self.safe_float(ticker, 'openPrice'),
            'close': last,
            'last': last,
            'previousClose': self.safe_float(ticker, 'prevClosePrice'),  # previous day close
            'change': self.safe_float(ticker, 'priceChange'),
            'percentage': self.safe_float(ticker, 'priceChangePercent'),
            'average': None,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'info': ticker,
        }

    def fetch_status(self, params={}):
        response = self.wapiGetSystemStatus(params)
        status = self.safe_value(response, 'status')
        if status is not None:
            status = 'ok' if (status == 0) else 'maintenance'
            self.status = self.extend(self.status, {
                'status': status,
                'updated': self.milliseconds(),
            })
        return self.status

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
        }
        method = 'publicGetTicker24hr' if market['spot'] else 'fapiPublicGetTicker24hr'
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_ticker(response, market)

    def parse_tickers(self, rawTickers, symbols=None):
        tickers = []
        for i in range(0, len(rawTickers)):
            tickers.append(self.parse_ticker(rawTickers[i]))
        return self.filter_by_array(tickers, 'symbol', symbols)

    def fetch_bids_asks(self, symbols=None, params={}):
        self.load_markets()
        defaultType = self.safe_string_2(self.options, 'fetchOpenOrders', 'defaultType', 'spot')
        type = self.safe_string(params, 'type', defaultType)
        query = self.omit(params, 'type')
        method = 'publicGetTickerBookTicker' if (type == 'spot') else 'fapiPublicGetTickerBookTicker'
        response = getattr(self, method)(query)
        return self.parse_tickers(response, symbols)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        method = self.options['fetchTickersMethod']
        response = getattr(self, method)(params)
        return self.parse_tickers(response, symbols)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            ohlcv[0],
            float(ohlcv[1]),
            float(ohlcv[2]),
            float(ohlcv[3]),
            float(ohlcv[4]),
            float(ohlcv[5]),
        ]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            'interval': self.timeframes[timeframe],
        }
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit  # default == max == 500
        method = 'publicGetKlines' if market['spot'] else 'fapiPublicGetKlines'
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        if 'isDustTrade' in trade:
            return self.parse_dust_trade(trade, market)
        #
        # aggregate trades
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#compressedaggregate-trades-list
        #
        #     {
        #         "a": 26129,         # Aggregate tradeId
        #         "p": "0.01633102",  # Price
        #         "q": "4.70443515",  # Quantity
        #         "f": 27781,         # First tradeId
        #         "l": 27781,         # Last tradeId
        #         "T": 1498793709153,  # Timestamp
        #         "m": True,          # Was the buyer the maker?
        #         "M": True           # Was the trade the best price match?
        #     }
        #
        # recent public trades and old public trades
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#recent-trades-list
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#old-trade-lookup-market_data
        #
        #     {
        #         "id": 28457,
        #         "price": "4.00000100",
        #         "qty": "12.00000000",
        #         "time": 1499865549590,
        #         "isBuyerMaker": True,
        #         "isBestMatch": True
        #     }
        #
        # private trades
        # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#account-trade-list-user_data
        #
        #     {
        #         "symbol": "BNBBTC",
        #         "id": 28457,
        #         "orderId": 100234,
        #         "price": "4.00000100",
        #         "qty": "12.00000000",
        #         "commission": "10.10000000",
        #         "commissionAsset": "BNB",
        #         "time": 1499865549590,
        #         "isBuyer": True,
        #         "isMaker": False,
        #         "isBestMatch": True
        #     }
        #
        # futures trades
        # https://binance-docs.github.io/apidocs/futures/en/#account-trade-list-user_data
        #
        #     {
        #       "accountId": 20,
        #       "buyer": False,
        #       "commission": "-0.07819010",
        #       "commissionAsset": "USDT",
        #       "counterPartyId": 653,
        #       "id": 698759,
        #       "maker": False,
        #       "orderId": 25851813,
        #       "price": "7819.01",
        #       "qty": "0.002",
        #       "quoteQty": "0.01563",
        #       "realizedPnl": "-0.91539999",
        #       "side": "SELL",
        #       "symbol": "BTCUSDT",
        #       "time": 1569514978020
        #     }
        #
        timestamp = self.safe_integer_2(trade, 'T', 'time')
        price = self.safe_float_2(trade, 'p', 'price')
        amount = self.safe_float_2(trade, 'q', 'qty')
        id = self.safe_string_2(trade, 'a', 'id')
        side = None
        orderId = self.safe_string(trade, 'orderId')
        if 'm' in trade:
            side = 'sell' if trade['m'] else 'buy'  # self is reversed intentionally
        elif 'isBuyerMaker' in trade:
            side = 'sell' if trade['isBuyerMaker'] else 'buy'
        elif 'side' in trade:
            side = self.safe_string_lower(trade, 'side')
        else:
            if 'isBuyer' in trade:
                side = 'buy' if trade['isBuyer'] else 'sell'  # self is a True side
        fee = None
        if 'commission' in trade:
            fee = {
                'cost': self.safe_float(trade, 'commission'),
                'currency': self.safe_currency_code(self.safe_string(trade, 'commissionAsset')),
            }
        takerOrMaker = None
        if 'isMaker' in trade:
            takerOrMaker = 'maker' if trade['isMaker'] else 'taker'
        symbol = None
        if market is None:
            marketId = self.safe_string(trade, 'symbol')
            market = self.safe_value(self.markets_by_id, marketId)
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': orderId,
            'type': None,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': price * amount,
            'fee': fee,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['id'],
            # 'fromId': 123,    # ID to get aggregate trades from INCLUSIVE.
            # 'startTime': 456,  # Timestamp in ms to get aggregate trades from INCLUSIVE.
            # 'endTime': 789,   # Timestamp in ms to get aggregate trades until INCLUSIVE.
            # 'limit': 500,     # default = 500, maximum = 1000
        }
        defaultType = self.safe_string_2(self.options, 'fetchTrades', 'defaultType', 'spot')
        type = self.safe_string(params, 'type', defaultType)
        query = self.omit(params, 'type')
        defaultMethod = 'fapiPublicGetTrades' if (type == 'future') else 'publicGetTrades'
        method = self.safe_string(self.options, 'fetchTradesMethod', defaultMethod)
        if method == 'publicGetAggTrades':
            if since is not None:
                request['startTime'] = since
                # https://github.com/ccxt/ccxt/issues/6400
                # https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md#compressedaggregate-trades-list
                request['endTime'] = self.sum(since, 3600000)
            if type == 'future':
                method = 'fapiPublicGetAggTrades'
        elif (method == 'publicGetHistoricalTrades') and (type == 'future'):
            method = 'fapiPublicGetHistoricalTrades'
        if limit is not None:
            request['limit'] = limit  # default = 500, maximum = 1000
        #
        # Caveats:
        # - default limit(500) applies only if no other parameters set, trades up
        #   to the maximum limit may be returned to satisfy other parameters
        # - if both limit and time window is set and time window contains more
        #   trades than the limit then the last trades from the window are returned
        # - 'tradeId' accepted and returned by self method is "aggregate" trade id
        #   which is different from actual trade id
        # - setting both fromId and time window results in error
        response = getattr(self, method)(self.extend(request, query))
        #
        # aggregate trades
        #
        #     [
        #         {
        #             "a": 26129,         # Aggregate tradeId
        #             "p": "0.01633102",  # Price
        #             "q": "4.70443515",  # Quantity
        #             "f": 27781,         # First tradeId
        #             "l": 27781,         # Last tradeId
        #             "T": 1498793709153,  # Timestamp
        #             "m": True,          # Was the buyer the maker?
        #             "M": True           # Was the trade the best price match?
        #         }
        #     ]
        #
        # recent public trades and historical public trades
        #
        #     [
        #         {
        #             "id": 28457,
        #             "price": "4.00000100",
        #             "qty": "12.00000000",
        #             "time": 1499865549590,
        #             "isBuyerMaker": True,
        #             "isBestMatch": True
        #         }
        #     ]
        #
        return self.parse_trades(response, market, since, limit)

    def parse_order_status(self, status):
        statuses = {
            'NEW': 'open',
            'PARTIALLY_FILLED': 'open',
            'FILLED': 'closed',
            'CANCELED': 'canceled',
            'PENDING_CANCEL': 'canceling',  # currently unused
            'REJECTED': 'rejected',
            'EXPIRED': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #  spot
        #
        #     {
        #         "symbol": "LTCBTC",
        #         "orderId": 1,
        #         "clientOrderId": "myOrder1",
        #         "price": "0.1",
        #         "origQty": "1.0",
        #         "executedQty": "0.0",
        #         "cummulativeQuoteQty": "0.0",
        #         "status": "NEW",
        #         "timeInForce": "GTC",
        #         "type": "LIMIT",
        #         "side": "BUY",
        #         "stopPrice": "0.0",
        #         "icebergQty": "0.0",
        #         "time": 1499827319559,
        #         "updateTime": 1499827319559,
        #         "isWorking": True
        #     }
        #
        #  futures
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "orderId": 1,
        #         "clientOrderId": "myOrder1",
        #         "price": "0.1",
        #         "origQty": "1.0",
        #         "executedQty": "1.0",
        #         "cumQuote": "10.0",
        #         "status": "NEW",
        #         "timeInForce": "GTC",
        #         "type": "LIMIT",
        #         "side": "BUY",
        #         "stopPrice": "0.0",
        #         "updateTime": 1499827319559
        #     }
        #
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbol = None
        marketId = self.safe_string(order, 'symbol')
        if marketId in self.markets_by_id:
            market = self.markets_by_id[marketId]
        if market is not None:
            symbol = market['symbol']
        timestamp = None
        if 'time' in order:
            timestamp = self.safe_integer(order, 'time')
        elif 'transactTime' in order:
            timestamp = self.safe_integer(order, 'transactTime')
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'origQty')
        filled = self.safe_float(order, 'executedQty')
        remaining = None
        # - Spot/Margin market: cummulativeQuoteQty
        # - Futures market: cumQuote.
        #   Note self is not the actual cost, since Binance futures uses leverage to calculate margins.
        cost = self.safe_float_2(order, 'cummulativeQuoteQty', 'cumQuote')
        if filled is not None:
            if amount is not None:
                remaining = amount - filled
                if self.options['parseOrderToPrecision']:
                    remaining = float(self.amount_to_precision(symbol, remaining))
                remaining = max(remaining, 0.0)
            if price is not None:
                if cost is None:
                    cost = price * filled
        id = self.safe_string(order, 'orderId')
        type = self.safe_string_lower(order, 'type')
        if type == 'market':
            if price == 0.0:
                if (cost is not None) and (filled is not None):
                    if (cost > 0) and (filled > 0):
                        price = cost / filled
                        if self.options['parseOrderToPrecision']:
                            price = float(self.price_to_precision(symbol, price))
        elif type == 'limit_maker':
            type = 'limit'
        side = self.safe_string_lower(order, 'side')
        fee = None
        trades = None
        fills = self.safe_value(order, 'fills')
        if fills is not None:
            trades = self.parse_trades(fills, market)
            numTrades = len(trades)
            if numTrades > 0:
                cost = trades[0]['cost']
                fee = {
                    'cost': trades[0]['fee']['cost'],
                    'currency': trades[0]['fee']['currency'],
                }
                for i in range(1, len(trades)):
                    cost = self.sum(cost, trades[i]['cost'])
                    fee['cost'] = self.sum(fee['cost'], trades[i]['fee']['cost'])
        average = None
        if cost is not None:
            if filled:
                average = cost / filled
                if self.options['parseOrderToPrecision']:
                    average = float(self.price_to_precision(symbol, average))
            if self.options['parseOrderToPrecision']:
                cost = float(self.cost_to_precision(symbol, cost))
        clientOrderId = self.safe_string(order, 'clientOrderId')
        return {
            'info': order,
            'id': id,
            'clientOrderId': clientOrderId,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'average': average,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        # the next 5 lines are added to support for testing orders
        method = 'privatePostOrder' if market['spot'] else 'fapiPrivatePostOrder'
        if market['spot']:
            test = self.safe_value(params, 'test', False)
            if test:
                method += 'Test'
                params = self.omit(params, 'test')
        uppercaseType = type.upper()
        request = {
            'symbol': market['id'],
            'type': uppercaseType,
            'side': side.upper(),
        }
        if uppercaseType == 'MARKET':
            quoteOrderQty = self.safe_float(params, 'quoteOrderQty')
            precision = market['precision']['price']
            if quoteOrderQty is not None:
                request['quoteOrderQty'] = self.decimal_to_precision(quoteOrderQty, TRUNCATE, precision,
                                                                     self.precisionMode)
                params = self.omit(params, 'quoteOrderQty')
            elif price is not None:
                request['quoteOrderQty'] = self.decimal_to_precision(amount * price, TRUNCATE, precision,
                                                                     self.precisionMode)
            else:
                request['quantity'] = self.amount_to_precision(symbol, amount)
        else:
            request['quantity'] = self.amount_to_precision(symbol, amount)
        if market['spot']:
            request['newOrderRespType'] = self.safe_value(self.options['newOrderRespType'], type,
                                                          'RESULT')  # 'ACK' for order id, 'RESULT' for full order or 'FULL' for order with fills
        timeInForceIsRequired = False
        priceIsRequired = False
        stopPriceIsRequired = False
        if uppercaseType == 'LIMIT':
            priceIsRequired = True
            timeInForceIsRequired = True
        elif (uppercaseType == 'STOP_LOSS') or (uppercaseType == 'TAKE_PROFIT'):
            stopPriceIsRequired = True
            if market['future']:
                priceIsRequired = True
        elif (uppercaseType == 'STOP_LOSS_LIMIT') or (uppercaseType == 'TAKE_PROFIT_LIMIT'):
            stopPriceIsRequired = True
            priceIsRequired = True
            timeInForceIsRequired = True
        elif uppercaseType == 'LIMIT_MAKER':
            priceIsRequired = True
        elif uppercaseType == 'STOP':
            stopPriceIsRequired = True
            priceIsRequired = True
        elif uppercaseType == 'STOP_MARKET':
            stopPriceIsRequired = True
        if priceIsRequired:
            if price is None:
                raise InvalidOrder(self.id + ' createOrder method requires a price argument for a ' + type + ' order')
            request['price'] = self.price_to_p
