#from cryptoquant.api.api_gateway.build.exchange import get_exchange
#from cryptoquant.api.api_gateway.exchange import get_exchange

from cryptoquant.api.api_gateway.pro.apigateway_v8 import ApiGateway,get_exchange
from sq_ccxt.ccxt_gateway2304 import CcxtGateway
# 这里需要自己导入自己的交易所API KEY
from cryptoquant.config.config import ok_api_key, ok_seceret_key, ok_passphrase,binance_api_key,binance_secret_key
from cryptoquant.app.log.logger import log_engine

def get_exchange(symbol, apikey, secret, time_frame, strategy_name, setting):
    trade_api = CcxtGateway(symbol, apikey, secret)
    logger = log_engine(strategy_name)
    # 实例化策略与交易所接口之间的中间通道类
    exchange = ApiGateway(trade_api, symbol, time_frame, strategy_name, logger, setting)
    return exchange



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
