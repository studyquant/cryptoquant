"""
web:  studyquant.com
author: Rudy
wechat:82789754
"""

from cryptoquant.api.okex.okex_spot_exchange import OkexSpotApi
from cryptoquant.app.cta_strategy import (
    CtaTemplate,
    # StopOrder,
    TickData,
    # BarData,
    # TradeData,
    # OrderData,
    # BarGenerator,
    # ArrayManager,
)
from cryptoquant.trader.constant import (
    Direction,
    # OrderType,
    # Interval,
    # Exchange,
    Offset,
    # Status
)
from cryptoquant.trader.object import OrderRequest, OrderType  # AccountData,
import pandas as pd


# 策略和交易所API 之间的通道，确保交易所调用返还的数据格式是策略需要的格式
# 我们希望我们的策略可以在多个交易所上可以正常运行。为了达到这个目的，我这里是专门写了一个通道的类，通过这个通道类，去调用交易所的接口，这样，以后所有的策略，都通过这个通道去调用数据就可以了。

class ApiGateway:

    def __init__(self, exchange):
        """
        Args:
            exchange: any exchange
        """
        self.exchange_gate = exchange

    def get_account(self, coin:str):

        return self.exchange_gate.get_coin_account_info(coin)

    def get_ticker(self, symbol) -> TickData:
        """
        获取TIcker 数据
        Args:
            symbol: symbol
        Returns:
        """
        return self.exchange_gate.GetTicker(symbol)

    def get_kline_data(self, symbol, time_frame) -> pd.DataFrame:
        """
        获取TIcker 数据
        Args:
            symbol: symbol
            time_frame: time_frame
        Returns:
        """
        return self.exchange_gate.get_kline_data(symbol, time_frame)

    def buy(self, symbol, price: float, volume: float, stop: bool = False, lock: bool = False, order_id: str = '',
            order_type=OrderType.LIMIT):
        """
        Send buy order to open a long position.
        """
        return self.exchange_gate.send_template_order(symbol, Direction.LONG, Offset.OPEN, price, volume, stop, lock,
                                                 order_id, order_type)

    def sell(self, symbol, price: float, volume: float, stop: bool = False, lock: bool = False, order_id='',
             order_type=OrderType.LIMIT):
        """
        Send sell order to open a long position.
        """
        return self.exchange_gate.send_template_order(symbol, Direction.SHORT, Offset.CLOSE, price, volume, stop, lock,
                                                 order_id, order_type)

    def short(self, symbol, price: float, volume: float, stop: bool = False, lock: bool = False, order_id='',
              order_type=OrderType.LIMIT):
        """
        Send short order to open a short position.
        """
        return self.exchange_gate.send_template_order(symbol, Direction.SHORT, Offset.OPEN, price, volume, stop, lock,
                                                 order_id, order_type)

    def sellshort(self, symbol, price: float, volume: float, stop: bool = False, lock: bool = False, order_id='',
                  order_type=OrderType.LIMIT):
        """
        Send buy order to close a short position.
        """
        return self.exchange_gate.send_template_order(symbol, Direction.LONG, Offset.CLOSE, price, volume, stop, lock,
                                                 order_id, order_type)

    def send_order(
            self,
            strategy: CtaTemplate,
            direction: Direction,
            offset: Offset,
            price: float,
            volume: float,
            stop: bool = False,
            lock: bool = False,
            customize_order_id: str = '',
            order_type=OrderType.LIMIT,
    ) -> dict:
        """
        下单
        :param direction: direction 方向
        :param offset: 开仓 还是 平仓
        :param price: price
        :param volume: volume
        :param stop: 是否是停损单
        :param lock: 是否锁仓
        :param customize_order_id: orderId
        :param order_type: limit_order or market_order
        :return: orderId
        """
        # contract = self.main_engine.get_contract(strategy.vt_symbol)
        # if not contract:
        #     self.write_log(f"委托失败，找不到合约：{strategy.vt_symbol}", strategy)
        #     return ""
        # # Round order price and volume to nearest incremental value
        # price = round_to(price, contract.pricetick)
        # volume = round_to(volume, contract.min_volume)
        req = OrderRequest(symbol=strategy.symbol,
                           offset=offset,
                           exchange=self.exchange_gate.exchange_name,
                           direction=direction,
                           type=order_type,
                           price=price,
                           volume=volume
                           )
        order_id = self.exchange_gate.send_serve_order(req)

        return order_id

    def cancel_all(self, strategy: CtaTemplate):
        """
        Cancel all active orders of a strategy.
        """
        # vt_orderids = self.strategy_orderid_map[strategy.strategy_name]
        # if not vt_orderids:
        #     return
        return self.exchange_gate.cancel_orders(strategy.symbol)

    # def cancel_all(self,instrument_id):
    #     return self.exchange_gate.cancel_orders(instrument_id)

if __name__ == "__main__":
    pass
