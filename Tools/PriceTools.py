# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 23:02

@desc:

'''

from decimal import Decimal


def toNearest(num, tickSize, smallestUnit=None):
    """Given a number, round it to the nearest tick. Very useful for sussing float error
       out of numbers: e.g. toNearest(401.46, 0.01) -> 401.46, whereas processing is
       normally with floats would give you 401.46000000000004.
       Use this after adding/subtracting/multiplying numbers."""
    tickDec = Decimal(str(tickSize))
    if smallestUnit:
        while smallestUnit < 1:
            smallestUnit *= 10
        num = Decimal(round(num / tickSize, 0))
        remainder = num % Decimal(smallestUnit)
        num -= remainder
        if remainder >= smallestUnit / 2:
            num += Decimal(smallestUnit)
        return float(num * tickDec)
    else:
        return float((Decimal(round(num / tickSize, 0)) * tickDec))
