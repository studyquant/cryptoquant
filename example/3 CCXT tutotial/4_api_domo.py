# -*- coding: utf-8 -*-
"""
=========================================================
* Powered by StudyQuant
* author: Rudy
* wechat:82789754
================更多课程代码，请查看课程目录===============================
* 更多量化示例代码可添加微信 studyquant88 领取 

* Product Page: https://studyquant.com
* Copyright 2022 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.


"""
from cryptoquant.config.config import ok_api_key, ok_seceret_key, ok_passphrase,binance_api_key,binance_secret_key
from cryptoquant import get_exchange

"""
Attention:
to run this code file , your python may need to be python3.9. It can be run by my environment
of  python 3.9. Hope you can run it successfully. Many Thanks 
"""

if __name__ == "__main__":
    setting ={
        'symbol':"EOS/USDT",
        'api_key':binance_api_key,
        'secret':binance_secret_key,
        'base_asset':'EOS',
        'quote_asset':'USDT',
        'sleep_time':5,
        'time_frame':'5m'
    }

    apikey = binance_api_key
    secret = binance_secret_key
    symbol = "EOS/USDT"
    time_frame = '5m'
    strategy_name = 'apidemo'

    exchange = get_exchange(symbol, apikey, secret, time_frame, strategy_name, setting)

    print('GEt Trades', exchange.GetTrades())
    print('GEt Ticker',exchange.GetTicker())
    print('GEt Depth',exchange.GetDepth())
    print('GetAccount',exchange.GetAccount())
    print('获取K线',exchange.GetKline(time_frame))
    print('get Orders',exchange.GetOrders())
    print('get open Orders',exchange.GetOpenOrders())

    # 买单
    buy_order = exchange.Buy(Price = 3,Amount = 4)
    print(f"获取订单{exchange.GetOrder(buy_order.id)}")

    # 撤单
    cancel_order = exchange.CancelOrder(buy_order.id)
    print(f"取消订单{cancel_order}")

    # 卖单
    sell_order = exchange.Sell(Price = 5,Amount = 4)
    print(f"获取订单{exchange.GetOrder(buy_order.id)}")

    # 撤单
    cancel_order = exchange.CancelOrder(sell_order.id)
    print(f"取消订单{cancel_order}")
