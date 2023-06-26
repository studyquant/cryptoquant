from cryptoquant.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)

# from cryptoquant.api.okex.okex_spot_exchange import OkexSpotApi
# from cryptoquant.config.config import ok_api_key, ok_seceret_key, ok_passphrase
# from cryptoquant.api.okex.spot_api import SpotAPI
# from cryptoquant.trader.object import OrderData, Direction, Exchange, Interval, Offset, Status, Product, OptionType, \
#     OrderType, TradeData, ContractData
from cryptoquant.trader.object import OrderData, Interval, OrderType, TradeData
from cryptoquant import (
    Direction,
    Exchange,
    Interval,
    Offset,
    OrderType,
    Ticker,
    Account,
    Runmode,
    SymbolType,
)
from datetime import datetime


class DoubleMaStrategy(CtaTemplate):
    author = ""

    fast_window = 10  # 快均线
    slow_window = 20  # 短均线

    fast_ma0 = 0.0
    fast_ma1 = 0.0
    slow_ma0 = 0.0
    slow_ma1 = 0.0
    symbol_type = SymbolType.SPOT  # 现货
    minmium_sell_amount = 0  # 最小卖出数量
    fixed_order_amount = 1  # 最小卖出数量
    test_mode = False
    active_orderids = []

    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1", "pos"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        for key, value in setting.items():
            self.__dict__[key] = value
        # super().__init__(OkexSpotApi, cta_engine)
        # OkexSpotApi.__init__(self, api)
        self.symbol = vt_symbol
        self.bg = BarGenerator(self.on_bar)
        # 这里使用的是5分钟K线
        self.bg15 = BarGenerator(self.on_bar, 5, self.on_15min_bar, Interval.MINUTE)
        self.am15 = ArrayManager()

        # 这里使用的是2小时K线
        # self.bg15 = BarGenerator(self.on_bar, 1, self.on_15min_bar,Interval.HOUR)
        # self.am15 = ArrayManager()

        self.am = ArrayManager()
        self.exchange = cta_engine

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")
        self.put_event()

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        # print(tick)
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        # self.bg5.update_bar(bar)
        self.bg15.update_bar(bar)
        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        # self.handle_data()
        # self.put_event()

    def on_15min_bar(self, bar: BarData):
        """
        MACD 交易策略
        :param bar:
        :return:
        """
        self.cancel_all()
        self.am15.update_bar(bar)
        if not self.am15.inited:
            return
        kline = self.am.get_dataframe()
        self.handle_data()

    def on_tick_data(self, tick: Ticker):
        """
        Callback of new tick data update.
        """
        # print(tick)
        # self.bg.update_tick(tick)

        # 实盘
        self.ticker = tick.__dict__
        self.High = self.ticker["High"]
        self.Low = self.ticker["Low"]
        self.Sell = self.ticker["Sell"]
        self.Buy = self.ticker["Buy"]
        self.Last = self.close = self.ticker["Last"]
        self.Volume = self.ticker["Volume"]

        # 如果测试状态为TRUE, 那么进入条件语句
        if self.test_mode == True:
            pct = 0.05
            self.Buy = self.Buy * (1 + pct)  # 买一价格
            self.Sell = self.Sell * (1 - pct)  # 卖一价格
            self.write_log("价格已经打了折扣,买一{},卖一{}".format(self.Buy, self.Sell))

    def on_account(self, account: Account):
        """把账户信息推送到这里"""
        # 期货的处理逻辑
        if self.symbol_type == SymbolType.FUTURES:
            # 期货的逻辑
            pass

        # 以下是现货的处理逻辑,目前还用不到
        elif self.symbol_type == SymbolType.SPOT:
            self.pos = account.Available_stocks
            self.Available_usdt = account.Available_balance
            self.Available_stocks = account.Available_stocks
            self.abletosell = self.pos * 0.99

            # 使用账户余额20%购买
            self.fixed_order_amount = (account.Available_balance / self.Last) * 0.2

        else:
            self.write_log("其他品种逻辑未定义")

    def on_kline(self, kline_df):
        """
        实盘交易调用K线函数
        :param kline_df:
        :return:
        """
        am = self.am
        am.close_array = kline_df["close"]
        am.high_array = kline_df["high"]
        am.low_array = kline_df["low"]
        am.open_array = kline_df["open"]
        self.handle_data_spot()

    def handle_data(self):
        """期货交易"""
        fast_ma = self.am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma[-1]
        self.fast_ma1 = fast_ma[-2]

        slow_ma = self.am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma[-1]
        self.slow_ma1 = slow_ma[-2]

        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1
        current_price = self.am.close_array[-1]

        if cross_over:
            # print("cross_over")
            if self.pos == 0:
                self.buy(current_price, 1)
            elif self.pos < 0:
                self.cover(current_price, 1)
                self.buy(current_price, 1)

        elif cross_below:
            if self.pos == 0:
                self.short(current_price, 1)
            elif self.pos > 0:
                self.sell(current_price, 1)
                self.short(current_price, 1)

    def handle_data_spot(self):
        # 现货交易
        # order_id = self.buy(6, 1, order_type=OrderType.LIMIT)
        fast_ma = self.am.sma(self.fast_window, array=True)
        self.fast_ma0 = fast_ma.iloc[-1]
        self.fast_ma1 = fast_ma.iloc[-2]
        slow_ma = self.am.sma(self.slow_window, array=True)
        self.slow_ma0 = slow_ma.iloc[-1]
        self.slow_ma1 = slow_ma.iloc[-2]
        # 金叉
        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        # 死叉
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1
        current_price = self.current_price = self.am.close_array.iloc[-1]

        if cross_over:
            print("金叉")
            # if self.pos < 1:
            # 如果持仓小于0.01 则买入
            self.buy(
                self.current_price, self.fixed_order_amount, order_type=OrderType.LIMIT
            )

        elif cross_below:
            print("死叉")
            if self.pos > self.minmium_sell_amount:
                self.sell(
                    self.current_price, self.pos * 0.98, order_type=OrderType.LIMIT
                )

        self.report()

    def report(self):
        """print run log"""
        self.write_log(
            f"{datetime.now()} - symbol:{self.symbol } - current_pos: {self.pos} -- current_price: {self.current_price} - {self.fixed_order_amount}"
        )
        variables = self.get_variables()
        self.write_log(f"variables :{  variables }")

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        self.active_orderids.append(order.orderid)
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass


if __name__ == "__main__":
    pass
    # from cryptoquant.api.okex.apigateway import ApiGateway
    # symbol = 'OKB-USDT'
    # minutes = '5m'
    #
    # api = SpotAPI(ok_api_key, ok_seceret_key, ok_passphrase,True)
    # exchange = OkexSpotApi(api)
    # new_exchange = ApiGateway(exchange)
    # # exchange.connect(crypto_setting)
    # strategy = DoubleMaStrategy(new_exchange, 'strategy_name',symbol, {})
    # # ticker = strategy.get_ticker(symbol)
    # # strategy.on_tick(ticker)
    # strategy.trading = True
    # data = strategy.buy(3,1)
    # print(data)

    # print(ticker)
