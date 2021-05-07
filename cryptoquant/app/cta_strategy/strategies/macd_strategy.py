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
import talib
from cryptoquant.trader.object import OrderData, Direction, Exchange, Interval, Offset, Status, Product, OptionType, \
    OrderType, TradeData, ContractData
# from cryptoquant.app.cta_signal.macd import Macd

class MacdStrategy(CtaTemplate):
    """"""
    author = "Rudy"



    shortperiod = 12 # 快线周期
    longperiod = 26  # 慢线周
    smoothperiod = 9  # Signal平滑周期

    fixed_size = 1
    # ATR参数
    atr_window = 30
    # ATR 的倍数
    sl_multiplier = 2.1

    # 参数
    parameters = ["shortperiod", "longperiod",
                  "smoothperiod", "atr_window",
                  "sl_multiplier"]
    # 变量
    variables = ["", "", "","","pos","signal"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        # self.bg5 = BarGenerator(self.on_bar, 5, self.on_5min_bar)
        # self.am5 = ArrayManager()

        self.bg15 = BarGenerator(self.on_bar, 60, self.on_15min_bar)
        self.am15 = ArrayManager()


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

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg5.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        # self.bg5.update_bar(bar)
        self.bg15.update_bar(bar)


    def on_5min_bar(self, bar: BarData):
        """"""

        self.am5.update_bar(bar)
        if not self.am5.inited:
            return

        # self.rsi_value = self.am5.rsi(self.rsi_window)
        self.put_event()

    # staticmethod
    def macd(self,kline, SHORTPERIODSHORTPERIOD, LONGPERIOD, SMOOTHPERIOD):
        """
        close# 收盘价
        SHORTPERIODSHORTPERIOD = 12 # 快线周期
        LONGPERIOD = 26  # 慢线周期
        SMOOTHPERIOD = 9  # Signal平滑周期
        返回交易信号
        """
        close = kline['close']
        macd, signal, self.hist = talib.MACD(close, SHORTPERIODSHORTPERIOD, LONGPERIOD,SMOOTHPERIOD)  # 短期MACD, 长期signal, # Hist,短线-长线
        return macd, signal, self.hist

    def signal(self):
        if self.hist.iloc[-2] < 0 and self.hist.iloc[-1] > 0:
            signal = 1
        elif self.hist.iloc[-2] > 0 and self.hist.iloc[-1] < 0:
            signal = -1
        else:
            signal = 0
        return signal


    def handle_data(self,kline):
        # 计算mace指标
        macd, signal, hist = self.macd(kline,12,26,9)
        signal = self.signal()

        current_price = kline['close'].iloc[-1]
        high_price = kline['high'].iloc[-1]
        low_price = kline['low'].iloc[-1]

        # 计算ATR
        self.atr_value = self.am15.atr(self.atr_window)

        # ------------策略逻辑 ------------------
        if self.pos == 0:
            if signal == 1:
                self.buy(current_price, 1)
            if signal == -1:
                self.short(current_price, 1)

        elif self.pos > 0:
            if signal == -1:
                self.sell(current_price, 1)
                self.short(current_price, 1)

        elif self.pos < 0:
            if signal == 1:
                self.cover(current_price, 1)
                self.buy(current_price, 1)

        # ------------仓位管理逻辑 ------------------
        if self.pos == 0:
            self.intra_trade_high = high_price
            self.intra_trade_low = low_price

        elif self.pos > 0:
            self.intra_trade_high = max(self.intra_trade_high, high_price)
            self.intra_trade_low = low_price

            self.long_stop = self.intra_trade_high - self.atr_value * self.sl_multiplier
            self.sell(self.long_stop, abs(self.pos), True)

            # if signal == -1:
            #     # self.cover(current_price, 1)
            #     self.sell(current_price, 1)
        elif self.pos < 0:
            self.intra_trade_high = high_price
            self.intra_trade_low = min(self.intra_trade_low, low_price)

            self.short_stop = self.intra_trade_low + self.atr_value * self.sl_multiplier
            self.cover(self.short_stop, abs(self.pos), True)


            # if signal == 1:
            #     # self.cover(current_price, 1)
            #     self.buy(current_price, 1)

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

        kline = self.am15.get_dataframe()
        self.handle_data(kline)


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
