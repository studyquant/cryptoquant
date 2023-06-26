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
from cryptoquant.config.config import binance_api_key,binance_secret_key
from cryptoquant.api.ccxt.ccxtgateway import CcxtGateway
from cryptoquant.api.api_gateway.apigateway_v7 import ApiGateway
from cryptoquant.app.datamodel.constant import Product,OrderStatus,Runmode,Direction,Offset,OrderType,OrderSTATUS,OrderOffset,Exchange
from cryptoquant.app.datamodel.data_model import Trade,Ticker,Record,OrderRequest,MarketOrder,Depth,Account,Position
from cryptoquant.app.log.logger import log_engine




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
    strategy_name = 'tesst'


    # exchange = get_exchange(symbol,apikey,secret,strategy_name,setting)
    trade_api = CcxtGateway(symbol,apikey,secret)
    logger = log_engine(strategy_name)
    # 实例化策略与交易所接口之间的中间通道类
    exchange = ApiGateway(trade_api,symbol,time_frame,strategy_name,logger,setting)
    logger = exchange.logger

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



    #
    # depth = exchange.GetDepth()
    # logger.info(depth)
    # # data = exchange.GetTrades()
    #
    # open_orders = exchange.GetOrders()
    # logger.info(open_orders)
    #
    # # 取消订单
    # for order in open_orders:
    #     exchange.CancelOrder(order.Id)
    #
    # # 获取持仓
    # position = exchange.GetPosition()
    # position.__dict__
    # logger.info(position)
    #
    # account,position = exchange.GetAccountPosition()
    # logger.info(account)
    # account.Balance
    #
    # # 持仓收益率
    # print('持仓收益率',position.UnrealizedReturnPct)
    #
    # # 总账户收益率
    # TotalPnlPct = account.TotalUnPnl / account.Balance
    # print('总账户收益率',TotalPnlPct)


    # order = exchange.buy(4, 4, order_type=OrderType.LIMIT)
    # logger.info(order)



    # logger.info(open_orders)


    # short_order = exchange.short(5, 4, order_type=OrderType.LIMIT)
    # logger.info(short_order)
    #
    # market_short_order = exchange.short(5, 4, order_type=OrderType.MARKET)
    # logger.info(market_short_order)
    #
    # market_buy_order = exchange.buy(5, 4, order_type=OrderType.MARKET)
    # logger.info(market_buy_order)
    # 限价单
    # order = exchange.SendOrder(3000,1,Direction = Direction.LONG.value,OrderType=OrderType.LIMIT.value)
    # logger.info(order)

    # # 市价单
    # order = exchange.SendOrder(3000,1,Direction = Direction.LONG.value,OrderType=OrderType.MARKET.value)
    # logger.info(order)


    # vnpy 接口测试
    #         strategy: CtaTemplate,
    #         direction: Direction,
    #         offset: Offset,
    #         price: float,
    #         volume: float,
    #         stop: bool = False,
    #         lock: bool = False,
    #         customize_order_id: str = '',
    #         order_type=OrderType.LIMIT,

    # order = exchange.send_order('any', direction = Direction.LONG,offset=Offset.OPEN,price=4,volume=4,order_type=OrderType.LIMIT)
    # logger.info(order)



