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
import time


class BrushFlowRobot(ExApiRobot):
    symbol = None
    min_amount = 0
    max_amount = 100
    amount_tick_size = 0
    stop_trade_times = 0

    start_time = None
    end_time = None

    normal_schedule_time = 5
    orderbook_schedule_time = 3  # orderbooks轮询时间(s)
    trades_schedule_time = 3
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

    async def __fetch_trades(self):
        if self.exapi:
            params = {'reverse': True} if 'bitmex' in self.exapi.id else {}
            self.trades = self.exapi.fetch_trades(self.symbol, params=params)
            self.logger.debug(self.trades)

    async def __create_order(self, symbol, type, side, amount, price=None, params={}):
        if self.exapi:
            order = self.exapi.create_order(symbol, type, side, amount, price, params)

    async def cancel_open_order_scheculer(self):
        fail_times = 0
        open_orders = self.exapi.exapi.fetch_open_orders(self.symbol)
        while self.is_ready and len(open_orders) > 0:
            try:
                now = int(time.time()) * 1000
                for order in self.open_orders:
                    if order['timestamp'] - now > 10000:
                        result = self.exapi.cancel_order(order['id'], self.symbol)
                        self.logger.info("cancel open order:%s, result:%s" % (order['id'], str(result)))
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch orderbook fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.normal_schedule_time)

    async def fetch_balance(self):
        fail_times = 0
        # now = int(time.time())
        # if now % (3600 * 24) > 5:
        #     return
        while self.is_ready:
            try:
                balance = self.exapi.fetch_balance()
                symbols = self.symbol.split('/')
                logging.info(
                    symbols[0] + ': ' + str(balance[symbols[0]]) + '\n' + symbols[1] + ': ' + str(balance[symbols[1]]))
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch orderbook fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.normal_schedule_time)

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
                await asyncio.sleep(self.normal_schedule_time)

    async def trades_scheduler(self):
        fail_times = 0
        while self.is_ready:
            try:
                await self.__fetch_trades()
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch trades fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.trades_schedule_time)

    async def main_scheduler(self):
        fail_times = 0
        loop = asyncio.get_event_loop()
        while self.is_ready:
            try:
                if self.orderbook == {} or self.trades == {}:
                    self.logger.info("Cache date is empty!")
                    continue

                p = self.module.need_to_trade(self.orderbook['bids'], self.orderbook['asks'], self.trades)
                if p and p > 0:
                    amount = random.uniform(self.min_amount, self.max_amount)
                    amount = price_tools.to_nearest(amount, self.amount_tick_size)
                    r = random.randint(0, 1)
                    side = 'buy' if r == 0 else 'sell'
                    reside = 'buy' if side == 'sell' else 'sell'
                    task1 = loop.create_task(self.__create_order(self.symbol, 'limit', side, amount, p))
                    task2 = loop.create_task(self.__create_order(self.symbol, 'limit', reside, amount, p))
                    # self.logger.info('**********ask:%s, bid:%s, price:%s, amount:%s**********' % (
                    #     str(self.orderbook['asks'][0][0]), str(self.orderbook['bids'][0][0]), str(p), str(amount)))
                    self.stop_trade_times = 0
                    if not loop.is_running():
                        loop.close()
                        loop.run_until_complete(asyncio.wait([task1, task2]))
                else:
                    self.stop_trade_times += 1
                fail_times = 0
            except BaseException as e:
                self.logger.error("main schedule run error:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                wait_time = random.randint(self.main_schedule_time[0], self.main_schedule_time[1])
                await asyncio.sleep(wait_time)

    async def open_disk_scheduler(self):
        fail_times = 0
        while self.is_ready:
            try:
                if self.stop_trade_times > 50:
                    bid1, ask1 = self.orderbook['bids'][0], self.orderbook['asks'][0]
                    amount = bid1[1] if bid1[1] < ask1[1] else ask1[1]
                    price = bid1[0] if bid1[1] < ask1[1] else ask1[0]
                    side = 'sell' if bid1[1] < ask1[1] else 'buy'
                    order = self.exapi.create_order(self.symbol, 'limit', side, amount, price)
                    self.logger.info('make open disk order: ' + str(order))
                    fail_times = 0
            except BaseException as e:
                self.logger.error("open_disk fail:%s" % (str(e)))
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
            task.append(asyncio.ensure_future(self.cancel_open_order_scheculer()))
            task.append(asyncio.ensure_future(self.fetch_balance()))
            task.append(asyncio.ensure_future(self.main_scheduler()))
            # task.append(asyncio.ensure_future(self.open_disk_scheduler()))
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
    exapi = public_tools.get_exapi("zg", {
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
        'min_amount': 100,
        'max_amount': 500,
        'amount_tick_size': 0.01,
        'orderbook_schedule_time': 2,
        'trades_schedule_time': 2,
        'order_schedule_time': 30,
        'main_schedule_time': [5, 15]
    })
    robot.start()
