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
print (ccxt.exchanges)
# from cryptoquant.config.config import binance_api_key,binance_secret_key

## 实例化交易所
# exchange = ccxt.binance({
#     'apiKey': binance_api_key,
#     'secret': binance_secret_key,
#     'timeout': 3000,
#     'enableRateLimit': True,
# })
symbol = 'BTC/USDT'
exchange = ccxt.binance({
    'apiKey': '',
    'secret': '',
    'timeout': 30000,
    'enableRateLimit': True,
})
# 第二种方式
# exchange_id = 'binance'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = exchange_class({
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET',
#     'timeout': 30000,
#     'enableRateLimit': True,
# })

tickers = exchange.fetch_tickers()
print('tickers',tickers)
### 获取市场信息
markets = exchange.load_markets()

symbol_info = markets[symbol]
precision = symbol_info['precision']

print(exchange.id, markets)

### 获取盘口信息

# print (exchange.fetch_order_book (symbol))
symbol = 'BTC/USDT'






orderbook = exchange.fetch_order_book (symbol)

print ('orderbook',orderbook)
print ('bids',orderbook['bids'])
print ('asks',orderbook['asks'])


# delay = 2 # seconds
# for symbol in exchange.markets:
#     print (exchange.fetch_order_book (symbol))
#     time.sleep (delay) # rate limit

### 获取TICKER数据
if (exchange.has['fetchTicker']):
    print('ticker',exchange.fetch_ticker(symbol)) # ticker for LTC/ZEC
    # symbols = list(exchange.markets.keys())
    # print(exchange.fetch_ticker(random.choice(symbols))) # ticker for a random symbol


### 获取K线数据
kline_data = exchange.fetch_ohlcv(symbol, '1d')
print('kline_data',kline_data)



# Python demo
# import time
# if exchange.has['fetchOHLCV']:
#     for symbol in exchange.markets:
#         time.sleep (exchange.rateLimit / 1000) # time.sleep wants seconds
#         print (symbol, exchange.fetch_ohlcv (symbol, '1d')) # one day

### 获取public trade线数据

public_trade = exchange.fetch_trades(symbol)
print('public_trade',public_trade)

# Python
# import time
# if exchange.has['fetchTrades']:
#     for symbol in exchange.markets:  # ensure you have called loadMarkets() or load_markets() method.
#         print (symbol, exchange.fetch_trades (symbol))



if __name__ == "__main__":
    pass
