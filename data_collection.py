# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2020/2/11 17:05

@desc:

'''
import time
import ccxt
from Tools import public_tools, redis_tools

hb = ccxt.huobipro()
exapi = public_tools.get_exapi("zg")
while True:
    now = int(time.time())
    if now % 300 == 0:
        eos = hb.fetch_ohlcv('EOS/USDT', '5m')
        eos_ohlcv = eos[-2]
        eosv = float(eos_ohlcv[5])

        eup = exapi.fetch_ohlcv('EUP/USDT', '5m')
        eup_ohlcv = eup[-2]
        eupv = float(eup_ohlcv[5])
        rate = eosv / eupv if eupv > 0 else 1
        redis_tools.set("EUP_USDTvolum_rate", rate)
        print(public_tools.get_time(), 'redis push data', rate)

