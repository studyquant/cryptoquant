"""
=========================================================
* Powered by StudyQuant
* author: Rudy
* wechat:82789754
=========================================================
"""

import pandas as pd
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import os
from cryptoquant.config.config import binance_api_key, binance_secret_key
import ccxt

# pd.set_option('display.max_rows', 500)		# 显示行数
pd.set_option('display.max_columns', 500)  # 显示列数
pd.set_option('display.width', 1000)  # 显示宽度

symbol = 'BTC/USDT'
exchange = ccxt.binance({
    'apiKey': '',
    'secret': '',
    'timeout': 30000,
    'enableRateLimit': True,
})

"""
自动交易简易的流程：  
根据个人的策略情况不同，自行调整



"""
def get_kline():
    print(f'{datetime.now()}:kline data')

if __name__ == "__main__":
    job_defaults = {'max_instances': 20}  # 最大任务数量
    scheduler = BackgroundScheduler(timezone='MST', job_defaults=job_defaults)


    # 每当第5秒的时候，买入
    scheduler.add_job(get_kline, 'cron', second="*/5")
    scheduler.add_job(get_kline, 'cron', minute="*/5")
    scheduler.start()

    while True:
        time.sleep(1)
