# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 23:02

@desc:

'''

from decimal import Decimal


def to_nearest(num, tick_size, smallest_unit=True):
    """Given a number, round it to the nearest tick. Very useful for sussing float error
       out of numbers: e.g. toNearest(401.46, 0.01) -> 401.46, whereas processing is
       normally with floats would give you 401.46000000000004.
       Use this after adding/subtracting/multiplying numbers."""
    tick_dec = Decimal(str(tick_size))
    # 最小单位四舍五入
    if smallest_unit:
        while smallest_unit < 1:
            smallest_unit *= 10
        num = Decimal(round(num / tick_size, 0))
        remainder = num % Decimal(smallest_unit)
        num -= remainder
        if remainder >= smallest_unit / 2:
            num += Decimal(smallest_unit)
        return float(num * tick_dec)
    else:
        return float((Decimal(round(num / tick_size, 0)) * tick_dec))
