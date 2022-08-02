import pandas as pd
import numpy as np
from datetime import datetime
import time

"""
=========================================================
* Powered by StudyQuant
* author: Rudy
* wechat:82789754
=========================================================
量化自动交易简易的流程：  
根据个人的策略情况不同，自行调整
"""


def get_kline():
    """
    获取K线数据
    """
    print(f'{datetime.now()}:kline data')


def get_account():
    """
    获取账户信息
    """
    print(f'{datetime.now()}:获取账户信息')


def order(symbol,direaction,amount):
    """
    下单
    """
    print(f'direction: {direaction}, symbol: {symbol}, amount{amount}')



def get_ma_signal(kline):
    """
    通过K线 计算下单信号
    :param kline
    """
    signal = 0
    print(f'signal: {signal}')
    return signal



def get_open_orders():
    """
    获取未成交的订单
    """
    data =None
    print(f'获取未成交的订单: {data}')


def cancel_order(order_id):
    """
    获取未成交的订单
    """
    print(f'取消订单id: {order_id}')


symbol = 'BTC_USDT'

def main():
    """
    策略流程
    """
    print("*"*10,'开始运行策略')
    get_open_orders()
    cancel_order(1)
    get_account()
    kline = get_kline()
    signal = get_ma_signal(kline)
    # signal1 - 买入，-1:卖出
    amount = 1 # 默认买一手
    order(symbol,signal,amount)


if __name__ == "__main__":
    while True:
        main()
        # 时间轮训的方式来运行
        time.sleep(2)
