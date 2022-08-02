"""
=========================================================
* Powered by StudyQuant
* author: Rudy
* wechat:82789754
=========================================================
* 更多量化示例代码可添加微信 studyquant88 领取 

* Product Page: https://studyquant.com
* Copyright 2022 StudyQuant
* License (https://studyquant.com/)
* Coded by https://studyquant.com
=========================================================
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""
"""
自动交易简易的流程：  
根据个人的策略情况不同，自行调整
 1 - 更新账户信息
 2 - 获取TICKER
 3 - 获取K线
 4 - 处理K线数据形成交易信号


 5 - 定时运行
    用户可参考代码添加定时运行模块，来完善，如需要完整脚本，可以添加微信 studyquant88 发送cryptoquant 来获取，这个示例应用的代码。
 wechat: studyquant88
"""
from cryptoquant import *
# - 策略导入
from cryptoquant.app.cta_strategy.strategies.double_ma_strategy import (
    DoubleMaStrategy
    )
from cryptoquant.config.strategy_config import ma_strategy_spot_setting
from squtils import sync_current_minute



def refresh_data(exchange, strategy:DoubleMaStrategy,time_frame):
    """
    更新数据
    """
    ticker = exchange.GetTicker()
    # 推送TICKER给策略
    strategy.on_tick_data(ticker)
    # 获取账户信息
    account = exchange.GetAccount()
    # # 推送到策略
    strategy.on_account(account)
    # 获取K线数据
    kline_df = exchange.GetKline(time_frame)
    strategy.on_kline(kline_df)


if __name__ == "__main__":
    # 参数设置
    setting = ma_strategy_spot_setting
    # symbol
    symbol = setting['symbol']
    # 策略
    strategy_name = 'Trend_strategy'
    # 策略周期
    time_frame = setting['time_frame']
    # API SECRET
    secret_key = setting['secret']
    # api_key
    api_key = setting['api_key']

    # 接口实例
    exchange = get_exchange(symbol, api_key, secret_key, time_frame, strategy_name, setting)
    exchange.log('开始运行')
    logger = exchange.logger

    # 策略实例
    strategy = DoubleMaStrategy(exchange, strategy_name, symbol, setting)
    strategy.trading = True  # 打开实盘交易
    strategy.fixed_order_amount = setting['order_amount']

    # 更新数据
    refresh_data(exchange,strategy,time_frame)

    """
    # todo
    后期可以添加定时运行模块，来完善，如需要完整脚本，可以添加微信 studyquant88 发送cryptoquant 来获取，这个示例应用的代码。
    """
    while True:
        refresh_data(exchange, strategy, time_frame)
        # 简易的时间驱动！ 用户可自行实现运行周期
        time.sleep(30)
