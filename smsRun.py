# ！/usr/bin/env python
# _*_ coding:utf-8 _*_

'''

@author: yerik

@contact: xiangzz159@qq.com

@time: 2019/12/3 17:27

@desc:

'''

import robots.kdj_notify_robot as kdjr
from Tools import public_tools

if __name__ == '__main__':
    exapi = public_tools.get_exapi("huobipro", {
        'enableRateLimit': False,
        'timeout': 20000,
        # 'proxies': {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
    })
    kdjr.main(exapi)

