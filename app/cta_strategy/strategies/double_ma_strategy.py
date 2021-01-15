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
from cryptoquant.api.okex.okex_spot_exchange import OkexSpotApi
from cryptoquant.config.config import ok_api_key, ok_seceret_key, ok_passphrase
from cryptoquant.api.okex.spot_api import SpotAPI




class DoubleMaStrategy(CtaTemplate):
    author = "用Python的交易员"

    fast_window = 10
    slow_window = 20

    fast_ma0 = 0.0
    fast_ma1 = 0.0

    slow_ma0 = 0.0
    slow_ma1 = 0.0

    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        # super().__init__(OkexSpotApi, cta_engine)
        # OkexSpotApi.__init__(self, api)
        self.symbol = vt_symbol
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

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
        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        self.handle_data()
        self.put_event()

    def on_kline(self,kline_df):
        """
        实盘交易调用K线函数
        :param kline_df:
        :return:
        """
        am = self.am
        am.close_array = kline_df['close']
        am.high_array = kline_df['high']
        am.low_array = kline_df['low']
        am.open_array = kline_df['open']
        self.handle_data()

    def handle_data(self):
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
            if self.pos < 0.01:
                self.buy(current_price, 1, order_type='market')

        elif cross_below:
            if self.pos > 0:
                self.sell(current_price, 1, order_type='market')


    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
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

if __name__=="__main__":

    from cryptoquant.api.okex.apigateway import ApiGateway
    symbol = 'OKB-USDT'
    minutes = '5m'

    api = SpotAPI(ok_api_key, ok_seceret_key, ok_passphrase,True)
    exchange = OkexSpotApi(api)
    new_exchange = ApiGateway(exchange)
    # exchange.connect(crypto_setting)
    strategy = DoubleMaStrategy(new_exchange, 'strategy_name',symbol, {})
    # ticker = strategy.get_ticker(symbol)
    # strategy.on_tick(ticker)
    strategy.trading = True
    data = strategy.buy(3,1)
    # print(data)









    # print(ticker)


