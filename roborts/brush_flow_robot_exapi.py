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


class BrushFlowRobot(object):
    exapi = None
    exws = None
    module = None
    symbol = None

    start_time = None
    end_time = None

    orderbook_schedule_time = 1  # orderbooks轮询时间(s)
    trades_schedule_time = 1
    order_schedule_time = 5
    cache_retention_time = 10  # 缓存数据留存时间(s)
    module_schedule_time = 1  # 策略轮询时间(s)

    is_ready = False
    fail_times_limit = 10

    # cache data
    orderbook = {}
    trades = {}
    open_orders = []
    history_orders = []
    history_orders_len = 1000

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
            # TODO 从exws类中获取
            # self.orderbook = self.exws.orderbook
            pass
        else:
            self.orderbook = self.exapi.fetch_order_book(self.symbol)
            self.logger.info(self.orderbook)

    async def __fetch_trades2cache(self):
        if self.exws:
            # TODO 从exws类中获取
            # self.trades = self.exws.trades
            pass
        else:
            params = {'reverse': True} if 'bitmex' in self.exapi.id else {}
            self.trades = self.exapi.fetch_trades(self.symbol, params=params)
            self.logger.info(self.trades)

    async def __fetch_openorder(self):
        if self.exws:
            # TODO 从exws类中获取
            self.open_orders = self.exws.open_orders
        else:
            open_orders = self.exapi.fetch_open_orders(self.symbol)
            open_order_ids = []
            for order in open_orders:
                open_order_ids.append(order['id'])
            for order in self.open_orders:
                if order['id'] not in open_order_ids:
                    if len(self.history_orders) > self.history_orders_len:
                        self.history_orders.remove()
                    self.history_orders.append(order)
                    self.logger.info("finished order:%s" % str(order))

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
                await self.__fetch_openorder()
                fail_times = 0
            except BaseException as e:
                self.logger.error("fetch trades fail:%s" % (str(e)))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.order_schedule_time)

    def async_task(self):
        loop = asyncio.get_event_loop()
        try:
            task = [asyncio.ensure_future(self.trades_scheduler()), asyncio.ensure_future(self.orderbook_scheduler())]
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
