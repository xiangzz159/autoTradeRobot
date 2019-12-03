# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 23:04

@desc:

'''

import time
from functools import wraps


def getTime():
    timestamp = time.time()
    time_local = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M", time_local)


# K线拟合
# @kline:k线队列
# @n:撮合数量
# @fittingTime:撮合时间周期
def klineFitting(kline, n, fittingTime):
    # 毫秒时间戳转化为秒
    st = kline[0][0]
    st = int(st - st % fittingTime) + fittingTime
    idx = 0
    for i in range(len(kline)):
        t = kline[i][0]
        if int(t) == st:
            idx = i
            break
    kline = kline[idx:]
    num = len(kline) % n
    kline = kline[:len(kline) - num]

    l = []
    for i in range(0, len(kline), n):
        ts = kline[i][0]
        open = kline[i][1]
        high = kline[i][2]
        for j in range(i + 1, i + n):
            high = max(high, kline[j][2])
        low = kline[i][3]
        for j in range(i + 1, i + n):
            low = min(low, kline[j][3])
        close = kline[i + n - 1][4]
        volumn = 0
        for j in range(i, i + n):
            volumn += kline[j][5]
        l.append([ts, open, high, low, close, volumn])
    return l


# 装饰器:计算函数耗时
def funcTimer(func):
    @wraps(func)
    def functionTimer(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print('\n', getTime(), "Total time running %s: %s seconds" %
              (func.__name__, str(t1 - t0)))
        return result

    return functionTimer
