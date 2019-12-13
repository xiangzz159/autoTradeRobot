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
from robots.robot import ExApiRobot
from modules.brush_flow import BrushFlow


class BrushFlowRobot(ExApiRobot):
    symbol = None
    min_amount = 0
    max_amount = 100
    amount_tick_size = 0

    start_time = None
    end_time = None

    orderbook_schedule_time = 5  # orderbooks轮询时间(s)
    trades_schedule_time = 5
    order_schedule_time = 30
    main_schedule_time = [30, 60]

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

    def __clear_cache(self):
        self.orderbook = {}
        self.trades = {}
        self.open_orders = []
        self.history_orders = []

    async def __fetch_orderbook2cache(self):
        if self.exapi:
            self.orderbook = self.exapi.fetch_order_book(self.symbol)
            self.logger.debug(self.orderbook)

    async def __fetch_trades2cache(self):
        if self.exapi:
            params = {'reverse': True} if 'bitmex' in self.exapi.id else {}
            self.trades = self.exapi.fetch_trades(self.symbol, params=params)
            self.logger.debug(self.trades)

    async def __fetch_orders(self):
        if self.exapi:
            orders = self.exapi.fetch_orders(self.symbol)
            self.logger.debug(orders)
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
        self.logger.info("create order: " + str(order))
        # self.open_orders.append(order)

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
                self.logger.error("fetch order fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.order_schedule_time)

    async def main_scheduler(self):
        fail_times = 0
        loop = asyncio.get_event_loop()
        while self.is_ready:
            try:
                if self.orderbook == {} or self.trades == {}:
                    self.logger.info("Cache date is empty!")
                    continue

                p = self.module.need_to_trade(self.orderbook['bids'], self.orderbook['asks'], self.trades)
                self.logger.info('**********ask:%s, bid:%s, price:%s**********' % (
                str(self.orderbook['asks'][0][0]), str(self.orderbook['bids'][0][0]), str(p)))
                if p and p > 0:
                    amount = random.uniform(self.min_amount, self.max_amount)
                    amount = price_tools.to_nearest(amount, self.amount_tick_size)
                    r = random.randint(0, 1)
                    side = 'buy' if r == 0 else 'sell'
                    reside = 'buy' if side == 'sell' else 'sell'
                    task1 = loop.create_task(self.__create_order(self.symbol, 'limit', side, amount, p))
                    task2 = loop.create_task(self.__create_order(self.symbol, 'limit', reside, amount, p))
                    if not loop.is_running():
                        loop.close()
                        loop.run_until_complete(asyncio.wait([task1, task2]))
                fail_times = 0
            except BaseException as e:
                self.logger.error("main schedule run error:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                wait_time = random.randint(self.main_schedule_time[0], self.main_schedule_time[1])
                await asyncio.sleep(wait_time)

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
            self.logger.info("**********Start brush flow robot!**********")
            task = []
            task.append(asyncio.ensure_future(self.trades_scheduler()))
            task.append(asyncio.ensure_future(self.orderbook_scheduler()))
            task.append(asyncio.ensure_future(self.main_scheduler()))
            # task.append(asyncio.ensure_future(self.order_scheduler()))
            self.async_task(task)
        except BaseException as e:
            self.logger.error("async task run error:%s" % (str(e)))
        finally:
            self.exit()

    def exit(self):
        self.is_ready = False
        self.__clear_cache()


def main():
    exapi = public_tools.get_exapi("bitmex", {
        'apiKey': '',
        'secret': '',
        'enableRateLimit': False,
        'timeout': 20000,
        # 'proxies': {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    })
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    module = BrushFlow(0.0001, 0.0001)
    module.logger = logger
    robot = BrushFlowRobot(exapi, module, {
        'symbol': 'EUP/USDT',
        'logger': logger,
        'min_amount': 20,
        'max_amount': 100,
        'amount_tick_size': 0.01,
        'orderbook_schedule_time': 2,
        'trades_schedule_time': 2,
        'order_schedule_time': 30,
        'main_schedule_time': [5, 15]
    })
    robot.start()
