# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2020/12/2 11:07

@desc:

'''

from stockstats import StockDataFrame
import numpy as np
import pandas as pd

def analyze(kline):
    df = pd.DataFrame(kline, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    stock = StockDataFrame.retype(df)
    df['signal'] = 'wait'
    stock['kdjk']

    # k上穿d时做多
    df['signal'] = np.where(
        (df['signal'] == 'wait') & (df['kdjk'].shift(1) < df['kdjd'].shift(1)) & (df['kdjk'] > df['kdjd']), 'long',
        df['signal'])

    # k下穿d时做空
    df['signal'] = np.where(
        (df['signal'] == 'wait') & (df['kdjk'].shift(1) > df['kdjd'].shift(1)) & (df['kdjk'] < df['kdjd']), 'short',
        df['signal'])

    return df.iloc[-1]


