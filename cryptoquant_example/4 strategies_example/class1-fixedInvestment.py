"""
=========================================================
* Powered by StudyQuant 
* author: Rudy
* wechat:studyquant88
=========================================================
* Product Page: https://studyquant.com
* Copyright 2021 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import os
from cryptoquant.config.config import binance_api_key, binance_secret_key
import ccxt

'''
    year (int|str) – 4-digit year
    month (int|str) – month (1-12)
    day (int|str) – day of the (1-31)
    week (int|str) – ISO week (1-53)
    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    hour (int|str) – hour (0-23)
    minute (int|str) – minute (0-59)
    second (int|str) – second (0-59)
    
    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
    
    *    any    Fire on every value
    */a    any    Fire every a values, starting from the minimum
    a-b    any    Fire on any value within the a-b range (a must be smaller than b)
    a-b/c    any    Fire every c values within the a-b range
    xth y    day    Fire on the x -th occurrence of weekday y within the month
    last x    day    Fire on the last occurrence of weekday x within the month
    last    day    Fire on the last day within the month
    x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
'''
exchange = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_secret_key,
    'timeout': 3000,
    'enableRateLimit': True,
    "options": {'recvWindow': 50000}
})


# 模仿购买股票函数
def buy(symbol, amount):
    ticker = exchange.fetch_ticker(symbol)
    sell_price = ticker['ask'] - 1
    print(f"{symbol} ask price {sell_price}")
    # 开始下单购买 B
    order_info = exchange.create_limit_buy_order(symbol, amount, sell_price)
    print(f"Buy {symbol} @{sell_price} Amount:{amount} id:{order_info['id']} time:{datetime.now()}")


def tick():
    print("tick", datetime.now())


def main():
    # 定时 cron 任务也非常简单，直接给触发器 trigger 传入 ‘cron’ 即可。hour =19 ,minute =23 这里表示每天的19：23 分执行任务。这里可以填写数字，也可以填写字符串
    job_defaults = {'max_instances': 20}  # 最大任务数量
    scheduler = BackgroundScheduler(timezone='MST', job_defaults=job_defaults)
    scheduler.add_job(tick, 'cron', minute="*", second='*/3')
    # 每分0秒定投买入
    # scheduler.add_job(buy, 'cron', minute="*", second='0',args=[eos,3])
    # scheduler.add_job(buy, 'cron', minute="*", second='0',args=[eos,3])
    # 每5秒买入一次
    # scheduler.add_job(buy, 'cron',  second='*/5',args=[symbol,3])
    # 每月1号定投买入 EOS
    scheduler.add_job(buy, 'cron', year="*", month='*', day='1', second="0", args=[symbol1, amount])
    # 每月1号定投买入 ETH
    scheduler.add_job(buy, 'cron', year="*", month='*', day='1', second="0", args=[symbol2, 0.1])
    # 每周第一天定投买入
    scheduler.add_job(buy, 'cron', day_of_week='1', second='0', args=[symbol1, 3])

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    symbol1 = 'EOS/USDT'
    amount = 3
    symbol2 = 'ETH/USDT'
    # buy(symbol,amount)
    main()

    while True:
        time.sleep(1)
