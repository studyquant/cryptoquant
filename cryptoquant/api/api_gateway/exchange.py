# from cryptoquant import CcxtGateway,ApiGateway

from cryptoquant.api.ccxt.build.ccxtgateway import CcxtGateway
from cryptoquant.api.api_gateway.build.apigateway_v7 import ApiGateway

from cryptoquant.app.log.logger import log_engine


def get_exchange(symbol, apikey, secret, time_frame, strategy_name, setting):
    trade_api = CcxtGateway(symbol, apikey, secret)
    logger = log_engine(strategy_name)
    # 实例化策略与交易所接口之间的中间通道类
    exchange = ApiGateway(trade_api, symbol, time_frame, strategy_name, logger, setting)
    # exchange = ApiGateway(trade_api, symbol, time_frame, strategy_name, logger, setting)
    return exchange
