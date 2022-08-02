"""
=========================================================
* author: rudy
=========================================================
"""

import pandas as pd
import numpy as np
from cryptoquant.config.config import binance_api_key, binance_secret_key
from cryptoquant import Interval, SymbolType, OrderType, Runmode

ma_strategy_setting = {
    "symbol": "ETHUSDT",  # 运行的品种
    "api_key": binance_api_key,
    "secret": binance_secret_key,
    "url": "https://fapi.binance.com",  # 接口的URL"https://fapi.binance.com"  "https://testnet.binancefuture.com"
    "quote_asset": "USDT",  # 标的USDT
    "time_frame": Interval.MIN5.value,  # 交易所设定的策略周期
    "sleep_time": 3,  # 策略轮询时间间隔
    "order_amount": 1,  # 回测- 下单数量，回测下单数量为1，实盘下单数量根据 资金*5% 计算
    "stop_pct": 0.03,  # 回测- 止损百分比
    "order_type": OrderType.MARKET,  # 下单类型，限价单还是市价，推荐市价
    "symbol_type": SymbolType.FUTURES,  # 标的类型，期货，还是现货
    "mode": Runmode.LIVE,  # 运行模式
    "test_mode": False,  # 是否测试策略模式, FALSE 为实盘， TRUE为测试
    "jiacang_times": 3,  # 加仓倍数
    "position_loss": 0.3,  # 持仓收益 小于-30% 止损
    "break_length": 20,  # 突破信号周期，默认二十
    "leverage": 5,  # 杠杆倍数
    "run_mode": Runmode.next_period,  # 次周期入场 还是 当前K线运行
    "order_amount_pct": 0.05,  # 下单为总资金的百分比
}


ma_strategy_spot_setting = {
    "symbol": "EOS/USDT",  # 运行的品种
    "api_key": binance_api_key,
    "secret": binance_secret_key,
    "url": "https://fapi.binance.com",  # 接口的URL"https://fapi.binance.com"  "https://testnet.binancefuture.com"
    "quote_asset": "USDT",  # 标的USDT
    "time_frame": Interval.MIN5.value,  # 交易所设定的策略周期
    "sleep_time": 3,  # 策略轮询时间间隔
    "order_amount": 10,  # 回测- 下单数量，回测下单数量为1，实盘下单数量根据 资金*5% 计算
    "order_type": OrderType.MARKET,  # 下单类型，限价单还是市价，推荐市价
    "symbol_type": SymbolType.SPOT,  # 标的类型，期货，还是现货
    "mode": Runmode.LIVE,  # 运行模式
    "test_mode": False,  # 是否测试策略模式, FALSE 为实盘， TRUE为测试
    "leverage": 5,  # 杠杆倍数
    "run_mode": Runmode.next_period,  # 次周期入场 还是 当前K线运行
}

if __name__ == "__main__":
    pass
