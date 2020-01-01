# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/9 09:31

@desc:

'''

import time
import logging
import random
from Tools import price_tools
from decimal import Decimal


class BrushFlow(object):

    def __init__(self, minumun_price, price_tick_size, logger=None):
        self.price_tick_size = price_tick_size
        self.minumun_price = minumun_price
        self.logger = logging.getLogger("root") if logger is None else logger

    def need_to_trade(self, bids, asks, trades):
        # 1. 盘口间有可挂单价格，用于同时下买卖单撮合
        # 2. 若10秒内有10笔订单，则此次不下单，避过下单高峰期
        t = int(time.time())
        trade_count = 0
        for trade in trades:
            if t - trade['timestamp'] / 1000 < 10:
                trade_count += 1
        if trade_count > 10:
            self.logger.debug("Trade count more than 10, stop trade")
            return None

        bid = bids[0][0]  # 买1
        ask = asks[0][0]  # 卖1
        if Decimal(str(ask)) - Decimal(str(bid)) == Decimal(str(self.minumun_price)):
            self.logger.debug("No insert price for disk, stop trade")
            return None

        p = random.uniform(bid + self.minumun_price, ask - self.minumun_price)
        return price_tools.to_nearest(p, self.price_tick_size, self.minumun_price)
