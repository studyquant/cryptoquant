"""
=========================================================
* author: rudy
策略可能需要用到的 函数
=========================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime


def crossover(a, b):
    """向上突破"""
    if a[-2] < b[-2] and a[-1] > b[-1]:
        return True
    else:
        return False


def crossunder(a, b):
    """向下突破"""
    if a[-2] > b[-2] and a[-1] < b[-1]:
        return True
    else:
        return False


def handle_kline_event(strategy, exchange, time_frame):
    """
    :param time_frame:  策略周期
    :return:
    """
    while True:
        try:
            kline_df = exchange.GetKline(time_frame)
            # 确保当前的最新K线时间 和 当前分钟线一致
            if kline_df["timestamp"].iloc[-1].minute == sync_current_minute(time_frame):
                # print('最新K线')
                # print(kline_df)
                break
            else:
                continue
            # 判断是否包含最新的数据
        except Exception as err:
            time.sleep(1)
            print(err)
        break
    strategy.on_kline(kline_df)


def sync_current_minute(time_frame):
    """
    同步当前时间周期
    :param time_frame: 时间周期： 分钟、小时
    :return:
    """
    if "m" in time_frame:
        """周期为分钟"""
        minutes = int(time_frame.strip("m"))
        now_time = datetime.now().minute

        # 如果当前时间周期能被整除,
        if now_time % minutes == 0:
            return now_time
        else:
            now_time -= now_time % minutes
            return now_time


def process_account_and_strategy_setting(api_accounts: dict, strategy_setting: dict) -> dict:
    """
    Args:
        api_accounts: dict, api accoutnt
        strategy_setting:

    Returns:

    """
    account_list = []
    all_accounts = {}

    for account_id, api_setting in api_accounts.items():
        # 只有账户 和 策略相同的 才会放在一起
        if api_setting['exchange'] == strategy_setting['exchange_name']:
            accounts = {}
            accounts.update(api_setting)
            accounts['strategy_name'] = "grid"
            if not hasattr(api_setting, "price_precise"):
                accounts['price_precise'] = 2
                accounts['volume_precise'] = 1
            accounts.update(strategy_setting)

            account_list.append(accounts)
            all_accounts[accounts['account_id']] = accounts
    return all_accounts


if __name__ == "__main__":
    sync_current_minute("5m")
    pass
