# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2020/12/2 09:40

@desc:

'''

import logging
import asyncio
import random
from robots.robot import ExApiRobot
from modules.TencentSMS import TencentSMS
import time
import traceback
from modules import KDJ


class KdjNotifyRobot(ExApiRobot):
    timeframes = ['15m', '30m', '1h', '4h']
    symbol = 'BTC/USD'
    normal_schedule_time = 5
    kline = {}
    notifies = {}
    notifyed = []
    template_id = None
    fail_times_limit = 10

    async def __fetch_ohlcv(self, timeframe='15m'):
        if self.exapi:
            kline = self.exapi.fetch_ohlcv(self.symbol, timeframe)
            kline_ = self.kline.get(timeframe)
            if kline_ is not None:
                if kline[-1][0] != kline_[-1][0]:
                    self.kline[timeframe] = kline
                    self.logger.info('update kline, key:%s' % timeframe)
            else:
                self.kline[timeframe] = kline
                self.logger.info('add kline, key:%s' % timeframe)
            self.logger.info("kline keys:%s" % str(self.kline.keys()))

    def __notify(self, *args):
        self.logger.info("send sms notify:" + args)

    async def notify_schedule(self):
        fail_times = 0
        while self.is_ready:
            for k in self.notifies.keys():
                v = self.notifies.get(k)
                if str(v.get('last_timestamp') + '-' + k) not in self.notifyed:
                    try:
                        # SMS通知
                        self.__notify(v['last_timestamp'], v['val1'], v['val2'], v['val3'], v['val4'], )
                        # 放入已通知列表
                        if len(self.notifyed) > 10:
                            self.logger.info("notifyed length is more than 10")
                            self.notifyed = self.notifyed[-10:]
                        self.logger.info("notifyed append key:%s" % (str(v.get('last_timestamp')) + '-' + k))
                        self.notifyed.append(v.get('last_timestamp') + '-' + k)
                    except:
                        self.logger.error("notify schedule fail:%s" % str(traceback.format_exc()))
                        fail_times += 1
                    finally:
                        self.is_ready = True if fail_times < self.fail_times_limit else False
                        await asyncio.sleep(1)

    async def kdj_schedule(self):
        while self.is_ready:
            self.logger.info("kdj_schedule keys:%s" % str(self.kline.keys))
            for k in self.kline.keys():
                kl = self.kline.get(k)
                self.logger.info("kdj_schedule-key:%s, kline:%s" % (k, str(kl[-1])))
                notify = self.notifies.get(k)
                if self.kline.get(k) is None:
                    continue
                if notify is not None and notify.get('last_timestamp') == kl[-1][0]:
                    continue
                row = KDJ.analyze(kl)
                self.logger.info('kdj_schedule-timestamp:%s, signal:%s' % (str(row['timestamp']), row['signal']) )
                if row['signal'] != 'wait':
                    signal = '金' if row['signal'] == 'long' else '死'
                    ex_name = self.exapi.id
                    self.notifies[k] = {
                        'val1': ex_name,
                        'val2': self.symbol,
                        'val3': signal,
                        'val4': k,
                        'last_timestamp': kl[-1][0]
                    }
                    self.logger.info("kdj_schedule-update notifies: %s" % str(self.notifies))
                try:
                    await asyncio.sleep(1)
                except:
                    self.logger.error("kdj schedule fail:%s" % str(traceback.format_exc()))

    async def ohlcv_schedule(self):
        fail_times = 0
        while self.is_ready:
            try:
                for timeframe in self.timeframes:
                    await self.__fetch_ohlcv(timeframe)
                    fail_times = 0
            except:
                self.logger.error("fetch ohlcv fail:%s" % str(traceback.format_exc()))
                fail_times += 1
            finally:
                self.is_ready = True if fail_times < self.fail_times_limit else False
                await asyncio.sleep(self.normal_schedule_time)

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
            self.logger.info("**********Start KDJ notify robot robot!**********")
            task = []
            task.append(asyncio.ensure_future(self.ohlcv_schedule()))
            task.append(asyncio.ensure_future(self.kdj_schedule()))
            task.append(asyncio.ensure_future(self.notify_schedule()))
            self.async_task(task)
        except:
            self.logger.error("async task run error:%s" % str(traceback.format_exc()))
        finally:
            self.exit()

    def exit(self):
        self.is_ready = False
        self.__clear_cache()


def main(exapi):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    module = TencentSMS('apikey', 'secret', 'xxxx', 'xxxx', ['+86184xxxxxxxx'])
    module.logger = logger
    robot = KdjNotifyRobot(exapi, module, {
        'logger': logger,
        'symbol': 'BTC/USDT',
        'template_id': '792028'
    })
    robot.start()
