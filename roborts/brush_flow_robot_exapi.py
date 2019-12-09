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
import asyncio
import random


class BrushFlowRobot(object):
    exapi = None
    exws = None
    module = None
    symbol = None
    min_amount = 0
    max_amount = 100
    amount_tick_size = 0

    start_time = None
    end_time = None

    orderbook_schedule_time = 1  # orderbooks轮询时间(s)
    trades_schedule_time = 1
    order_schedule_time = 5
    module_schedule_time = 1  # 策略轮询时间(s)
    main_schedule_time = 1

    is_ready = False
    fail_times_limit = 10

    # cache data
    orderbook = {}
    trades = []
    open_orders = []
    history_orders = []
    history_orders_len = 1000
    buy_amount = 0
    sell_amount = 0
    buy_price = 0
    sell_price = 0

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

    async def __fetch_orderbook2cache(self):
        # websocket数据存储，处理要在ws类中自己定义
        if self.exws:
            # 从exws类中获取
            # self.orderbook = self.exws.orderbook
            pass
        else:
            self.orderbook = self.exapi.fetch_order_book(self.symbol)
            self.logger.info(self.orderbook)

    async def __fetch_trades2cache(self):
        if self.exws:
            # 从exws类中获取
            # self.trades = self.exws.trades
            pass
        else:
            params = {'reverse': True} if 'bitmex' in self.exapi.id else {}
            self.trades = self.exapi.fetch_trades(self.symbol, params=params)
            self.logger.info(self.trades)

    async def __fetch_orders(self):
        if self.exws:
            # 从exws类中获取
            # self.open_orders = self.exws.open_orders
            pass
        else:
            orders = self.exapi.fetch_orders(self.symbol)
            open_order_ids = []
            for order in self.open_orders:
                open_order_ids.append(order['id'])

            # open/closed/rejected/canceled/expired
            for order in orders:
                if order['status'] == 'open':
                    continue
                elif order['status'] == 'closed':
                    if order['id'] in open_order_ids:
                        idx = open_order_ids.index(order['id'])
                        open_order_ids.pop(idx)
                        self.open_orders.pop(idx)
                        if len(self.history_orders) > self.history_orders_len:
                            self.history_orders.pop(0)
                        self.history_orders.append(order)
                        self.logger.info("finished order:%s" % str(order))
                elif order['status'] == 'canceled':
                    if order['id'] in open_order_ids:
                        idx = open_order_ids.index(order['od'])
                        open_order_ids.pop(idx)
                        self.open_orders.pop(idx)

    async def __create_order(self, symbol, type, side, amount, price=None, params={}):
        order = self.exapi.create_order(symbol, type, side, amount, price, params)
        self.open_orders.append(order)

    async def orderbook_scheduler(self):
        fail_times = 0
        while self.is_ready:
            try:
                await self.__fetch_orderbook2cache()
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch orderbook fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.orderbook_schedule_time)

    async def trades_scheduler(self):
        fail_times = 0
        while self.is_ready:
            try:
                await self.__fetch_trades2cache()
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch trades fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.trades_schedule_time)

    async def order_scheduler(self):
        fail_times = 0
        while self.is_ready:
            try:
                await self.__fetch_orders()
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch trades fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.order_schedule_time)

    async def main_scheduler(self):
        fail_times = 0
        while self.is_ready:
            try:
                if self.orderbook == {} or self.trades == {}:
                    self.logger.info("Cache date is empty!")
                    continue

                p = self.module.need_to_trade(self.orderbook['bids'], self.orderbook['asks'], self.trades)
                if p and p > 0:
                    amount = random.uniform(self.min_amount, self.max_amount)
                    amount = price_tools.to_nearest(amount, self.amount_tick_size)
                    loop = asyncio.get_event_loop()
                    create_order_task = [
                        asyncio.ensure_future(self.__create_order(self.symbol, 'limit', 'buy', amount, p)),
                        asyncio.ensure_future(self.__create_order(self.symbol, 'limit', 'sell', amount, p))]
                    loop.run_until_complete(create_order_task)
                    loop.close()
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch trades fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.main_schedule_time)

    def async_task(self):
        loop = asyncio.get_event_loop()
        try:
            task = [asyncio.ensure_future(self.trades_scheduler()), asyncio.ensure_future(self.orderbook_scheduler()),
                    asyncio.ensure_future(self.main_scheduler()), asyncio.ensure_future(self.order_scheduler())]
            loop.run_until_complete(asyncio.gather(*task))
        except BaseException as e:
            self.logger.error("async task run error:%s" % (str(e)))
        finally:
            loop.close()

    def start(self):
        # 检查所需模块
        if not (self.exapi or self.exws):
            self.logger.error("exapi or exws can not be empty!")
            return
        if not self.module:
            self.logger.error("module can not be empty!")
            return
        if not self.symbol:
            self.logger.error("symbol can not be empty!")
            return
        try:
            self.is_ready = True
            self.logger.info("Start brush flow robot!")
            self.async_task()
        except BaseException as e:
            self.logger.error("async task run error:%s" % (str(e)))
        finally:
            self.exit()

    def exit(self):
        self.is_ready = False
        # 取消所有订单
        self.exapi.cancel_all_orders()
        # 平仓
        self.exapi.close_position(self.symbol)
        self.__clear_cache()

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
