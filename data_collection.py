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
    eos = hb.fetch_ohlcv('EOS/USDT', '5m')
    eos_ohlcv = eos[-1]
    eosv = float(eos_ohlcv[5])
    eup = exapi.fetch_ohlcv('EUP/USDT', '5m')
    eup_ohlcv = eup[-1]
    eupv = float(eup_ohlcv[5])
    rate = eosv / eupv if eupv > 0 else 1
    redis_tools.setval("EUP_USDTvolum_rate", rate)
    time.sleep(1)
    time.sleep(20)
