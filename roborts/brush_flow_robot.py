# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 17:22

@desc: 刷量机器人

'''

import time
from Tools import public_tools, price_tools
import logging


class BrushFlowRobot(object):
    exapi = None
    exws = None
    module = None
    start_time = None
    end_time = None
    orderbook_schedule_time = 0  # orderbooks轮询时间(s)
    trades_schedule_time = 0
    cache_retention_time = 10  # 缓存数据留存时间(s)
    module_schedule_time = 1  # 策略轮询时间(s)
    is_ready = False
    fail_times_limit = 10
    # cache data
    orderbook = {}
    trades = {}
    open_orders = []
    history_orders = []
    symbol = None

    def __init__(self, exapi, module, params={}):
        self.exapi = exapi
        self.module = module
        self.logger = logging.getLogger('root')
        for key in params:
            if hasattr(self, key) and isinstance(getattr(self, key), dict):
                setattr(self, key, self.deep_extend(getattr(self, key), params[key]))
            else:
                setattr(self, key, params[key])

    def __clear_cache(self):
        self.orderbook = {}
        self.trades = {}
        self.open_orders = []
        self.history_orders = []

    def __fetch_orderbook2cache(self):
        # websocket数据存储，处理要在ws类中自己定义
        if self.exws:
            # TODO 从exws类中获取
            # self.orderbook = self.exws.orderbook
            pass
        else:
            self.orderbook = self.exapi.fetch_order_book(self.symbol)

    def __fetch_trades2cache(self):
        if self.exws:
            # TODO 从exws类中获取
            # self.trades = self.exws.trades
            pass
        else:
            self.trades = self.exapi.fetch_trades(self.symbol)

    def orderbook_scheduler(self):
        if self.exapi is None and self.exws is None:
            self.logger.error("[%s] exapi and exws not loaded!" % public_tools.get_time())
        fail_times = 0
        while self.is_ready:
            try:
                self.__fetch_orderbook2cache()
                fail_times = 0
            except BaseException as e:
                self.logger.error("[%s] fetch orderbook fail:" % public_tools.get_time(), e[0], e[1])
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                time.sleep(self.orderbook_schedule_time)

    def trades_scheduler(self):
        if self.exapi is None and self.exws is None:
            self.logger.error("[%s] exapi and exws not loaded!" % public_tools.get_time())
        fail_times = 0
        while self.is_ready:
            try:
                self.__fetch_trades2cache()
                fail_times = 0
            except BaseException as e:
                self.logger.error("[%s] fetch trades fail:" % public_tools.get_time(), e[0], e[1])
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                time.sleep(self.orderbook_schedule_time)

    def start(self):
        pass

    def exit(self):
        pass

    @staticmethod
    def deep_extend(*args):
        result = None
        for arg in args:
            if isinstance(arg, dict):
                if not isinstance(result, dict):
                    result = {}
                for key in arg:
                    result[key] = BrushFlowRobot.deep_extend(result[key] if key in result else None, arg[key])
            else:
                result = arg
