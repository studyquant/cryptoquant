"""
=========================================================
* Powered by StudyQuant 
* author: Rudy
* wechat:82789754
=========================================================
* Product Page: https://studyquant.com
* Copyright 2021 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
import time
import ccxt
# print (ccxt.exchanges)
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', 50)


# from cryptoquant.config.config import binance_api_key,binance_secret_key


if __name__ == "__main__":
    ## 实例化交易所
    exchange = ccxt.binance({
        'apiKey': '',
        'secret': '',
        'timeout': 30000,
        'enableRateLimit': True,
    })

    symbol = 'BTC/USDT'
    kline_data = exchange.fetch_ohlcv(symbol, '1d')
    # print('kline_data',kline_data)
    kline_df = pd.DataFrame(kline_data,columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    kline_df.index = pd.to_datetime(kline_df['time'], unit='ms')
    kline_df.loc[:, 'localminute'] = kline_df['time'].apply(lambda x :time.localtime(int(x/1000)))
    # kline_df.loc[:, 'timestamp'] = kline_df['localminute'].apply(lambda x :time.strftime("%Y-%m-%d %H:%M:%S", x))
    print(kline_df)





