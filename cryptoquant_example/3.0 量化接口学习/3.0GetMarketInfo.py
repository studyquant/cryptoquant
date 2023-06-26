#!/usr/bin/env python
# coding: utf-8

# ## StudyQuant

# In[14]:

import ccxt
import pandas as pd

## 实例化交易所
exchange = ccxt.binance({
    'apiKey': '',
    'secret': '',
    'timeout': 30000,
    'enableRateLimit': True,
})

# ## 获取TICKER
# 

# In[15]:


"""
{
    'symbol':        string symbol of the market ('BTC/USD', 'ETH/BTC', ...)
    'info':        { the original non-modified unparsed reply from exchange API },
    'timestamp':     int (64-bit Unix Timestamp in milliseconds since Epoch 1 Jan 1970)
    'datetime':      ISO8601 datetime string with milliseconds
    'high':          float, // highest price
    'low':           float, // lowest price
    'bid':           float, // current best bid (buy) price
    'bidVolume':     float, // current best bid (buy) amount (may be missing or undefined)
    'ask':           float, // current best ask (sell) price
    'askVolume':     float, // current best ask (sell) amount (may be missing or undefined)
    'vwap':          float, // volume weighed average price
    'open':          float, // opening price
    'close':         float, // price of last trade (closing price for current period)
    'last':          float, // same as `close`, duplicated for convenience
    'previousClose': float, // closing price for the previous period
    'change':        float, // absolute change, `last - open`
    'percentage':    float, // relative change, `(change/open) * 100`
    'average':       float, // average price, `(last + open) / 2`
    'baseVolume':    float, // volume of base currency traded for last 24 hours
    'quoteVolume':   float, // volume of quote currency traded for last 24 hours
}
"""

# In[16]:


symbol = 'BTC/USDT'
if (exchange.has['fetchTicker']):
    print('ticker', exchange.fetch_ticker(symbol))  # ticker for

# ## 获取K线数据

# In[17]:


### 获取K线数据
kline_data = exchange.fetch_ohlcv(symbol, '1m')
print('kline_data', kline_data)
kline_df = pd.DataFrame(kline_data)
print(kline_df)

# In[18]:


### 获取K线数据
kline_data = exchange.fetch_ohlcv(symbol, '1d')
print('kline_data', kline_data)
kline_df = pd.DataFrame(kline_data)
print(kline_df)

# ## 获取ORDERBOOK

# In[19]:


orderbook = exchange.fetch_order_book(symbol)
print('orderbook', orderbook)

# In[21]:


print('bids', orderbook['bids'])

# In[20]:


print('asks', orderbook['asks'])

# In[ ]:
