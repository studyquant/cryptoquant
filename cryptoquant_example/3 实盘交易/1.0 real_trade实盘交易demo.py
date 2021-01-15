"""
web:  studyquant.com
author: Rudy
wechat:82789754
"""
from cryptoquant.api.okex.okex_spot_exchange import OkexSpotApi
from cryptoquant.config.config import ok_api_key, ok_seceret_key, ok_passphrase
from cryptoquant.api.okex.spot_api import SpotAPI
from cryptoquant.api.api_gateway.apigateway import ApiGateway
from cryptoquant.app.cta_strategy.strategies.double_ma_strategy import DoubleMaStrategy
import schedule
import time
if __name__=="__main__":

    symbol = 'OKB-USDT'
    minutes = '5m'
    # 实例化OKEX接口的类
    api = SpotAPI(ok_api_key, ok_seceret_key, ok_passphrase, True)
    # 实例化自己封装好接口类
    api_gateway = OkexSpotApi(api)
    # 实例化策略与交易所接口之间的中间通道类
    exchange = ApiGateway(api_gateway)

    kline_df = exchange.get_kline_data(symbol, minutes)
    print(kline_df)
    ticker = exchange.get_ticker(symbol)
    print(ticker)
    # 买单
    order_data = exchange.buy(symbol,3,1)
    # 卖单
    # order_data = exchange.sell(symbol, 6, 1)
    # 卖单-限价
    # order_data = exchange.sell(symbol, 6, 1, order_id='sell')
    # 买单-市价单
    # order_data = exchange.buy(symbol, 6, 6, order_id='b', order_type=OrderType.MARKET)

