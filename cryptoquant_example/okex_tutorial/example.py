import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import okex.index_api as index
import okex.option_api as option
import okex.system_api as system
import json
import datetime
from setting import api_key,secret_key,passphrase
def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

time = get_timestamp()

if __name__ == '__main__':

    # param use_server_time's value is False if is True will use server timestamp
# account api test
# 资金账户API
    accountAPI = account.AccountAPI(api_key, secret_key, passphrase, False)
    # 资金账户信息 （6次/s）
    result = accountAPI.get_wallet()
    # 单一币种账户信息 （6次/s）
    result = accountAPI.get_currency('')
    # 资金划转  (1次/2s)
    # result = accountAPI.coin_transfer('', '', 1, 1, 5, sub_account='', instrument_id='', to_instrument_id='')
    # 提币 （6次/s）
    # result = accountAPI.coin_withdraw('', 1, 4, '', '', 0.0005)
    # 账单流水查询 （6次/s）
    # result = accountAPI.get_ledger_record()
    # 获取充值地址 （6次/s）
    # result = accountAPI.get_top_up_address('')
    # 获取账户资产估值 （1次/30s）
    # result = accountAPI.get_asset_valuation()
    # 获取子账户余额信息 （1次/30s）
    # result = accountAPI.get_sub_account('')
    # 查询所有币种的提币记录 （6次/s）
    # result = accountAPI.get_coins_withdraw_record()
    # 查询单个币种提币记录 （6次/s）
    # result = accountAPI.get_coin_withdraw_record('')
    # 获取所有币种充值记录 （6次/s）
    # result = accountAPI.get_top_up_records()
    # 获取单个币种充值记录 （6次/s）
    # result = accountAPI.get_top_up_record('')
    # 获取币种列表 （6次/s）
    # result = accountAPI.get_currencies()
    # 提币手续费 （6次/s）
    # result = accountAPI.get_coin_fee('')

# spot api test
# 币币API
    spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)
    # 币币账户信息 （20次/2s）
    result = spotAPI.get_account_info()
    # 单一币种账户信息 （20次/2s）
    # result = spotAPI.get_coin_account_info('')
    # 账单流水查询 （10次/2s）
    # result = spotAPI.get_ledger_record('')
    # 下单 （100次/2s）
    # result = spotAPI.take_order('', '', client_oid='', type='', price='', order_type='0', notional='', size='')

    # take orders
    # 批量下单 （50次/2s）
    # result = spotAPI.take_orders([
    #   {"instrument_id": "", "side": "", "type": "", "price": "", "size": ""},
    #   {"instrument_id": "", "side": "", "type": "", "price": "", "size": ""}
    # ])
    # 撤销指定订单 （100次/2s）
    # result = spotAPI.revoke_order('', '')

    # revoke orders
    # 批量撤销订单 （50次/2s）
    # result = spotAPI.revoke_orders([
    #     {'instrument_id': '', 'order_ids': ['', '']}
    # ])
    # 获取订单列表 （10次/2s）
    # result = spotAPI.get_orders_list('', '')
    # 获取所有未成交订单 （20次/2s）
    # result = spotAPI.get_orders_pending('')
    # 获取订单信息 （20次/2s）
    # result = spotAPI.get_order_info('', '')
    # 获取成交明细 （10次/2s）
    # result = spotAPI.get_fills('xrp-usdt', '')
    # 委托策略下单 （40次/2s）
    # result = spotAPI.take_order_algo('', '', '', '', '', trigger_price='', algo_price='', algo_type='')
    # 委托策略撤单 （20 次/2s）
    # result = spotAPI.cancel_algos('', [''], '')
    # 获取当前账户费率 （1次/10s）
    # result = spotAPI.get_trade_fee()
    # 获取委托单列表 （20次/2s）
    # result = spotAPI.get_order_algos('', '', status='', algo_id='')
    # 公共-获取币对信息 （20次/2s）
    # result = spotAPI.get_coin_info()
    # 公共-获取深度数据 （20次/2s）
    # result = spotAPI.get_depth('', '')
    # 公共-获取全部ticker信息 （20次/2s）
    # result = spotAPI.get_ticker()
    # 公共-获取某个ticker信息 （20次/2s）
    # result = spotAPI.get_specific_ticker('')
    # 公共-获取成交数据 （20次/2s）
    # result = spotAPI.get_deal('', limit='')
    # 公共-获取K线数据 （20次/2s）
    # result = spotAPI.get_kline('', '')

# level api test
# 币币杠杆API
    levelAPI = lever.LeverAPI(api_key, secret_key, passphrase, False)
    # 币币杠杆账户信息 （20次/2s）
    result = levelAPI.get_account_info()
    # 单一币对账户信息 （20次/2s）
    # result = levelAPI.get_specific_account('')
    # 账单流水查询 （10次/2s）
    # result = levelAPI.get_ledger_record('')
    # 杠杆配置信息 （20次/2s）
    # result = levelAPI.get_config_info()
    # 某个杠杆配置信息 （20次/2s）
    # result = levelAPI.get_specific_config_info('')
    # 获取借币记录 （20次/2s）
    # result = levelAPI.get_borrow_coin()
    # 某币对借币记录 （20次/2s）
    # result = levelAPI.get_specific_borrow_coin('')
    # 借币 （100次/2s）
    # result = levelAPI.borrow_coin('', '', '')
    # 还币 （100次/2s）
    # result = levelAPI.repayment_coin('', '', '')
    # 下单 （100次/2s）
    # result = levelAPI.take_order('', '', '', type='', price='', size='')

    # take orders
    # params = [
    #   {'instrument_id': '', 'side': '', 'type': '', 'notional': '', 'margin_trading': '2'},
    #   {'instrument_id': '', 'side': '', 'price': '', 'size': '', 'margin_trading': '2'}
    # ]
    # 批量下单 （50次/2s）
    # result = levelAPI.take_orders(params)
    # 撤销指定订单 （100次/2s）
    # result = levelAPI.revoke_order('', '')

    # revoke orders
    # params = [
    #   {'instrument_id': '', 'order_ids': ['', '']},
    #   {'instrument_id': '', 'client_oids': ['', '']}
    # ]
    # 批量撤销订单 （50次/2s）
    # result = levelAPI.revoke_orders(params)

    # 获取订单列表 （10次/2s）
    # result = levelAPI.get_order_list('', '')
    # 获取订单信息 （20次/2s）
    # result = levelAPI.get_order_info('', '')
    # 获取所有未成交订单 （20次/2s）
    # result = levelAPI.get_order_pending('')
    # 获取成交明细 （10次/2s）
    # result = levelAPI.get_fills('')
    # 获取杠杆倍数 （5次/2s）
    # result = levelAPI.get_leverage('')
    # 设置杠杆倍数 （5次/2s）
    # result = levelAPI.set_leverage('', '')
    # 公共-获取标记价格 （20次/2s）
    # result = levelAPI.get_mark_price('')

# future api test
# 交割合约API
    futureAPI = future.FutureAPI(api_key, secret_key, passphrase, False)
    # 所有合约持仓信息 （5次/2s）
    result = futureAPI.get_position()
    # 单个合约持仓信息 （20次/2s）
    # result = futureAPI.get_specific_position('')
    # 所有币种合约账户信息 （1次/10s）
    # result = futureAPI.get_accounts()
    # 单个币种合约账户信息 （20次/2s）
    # result = futureAPI.get_coin_account('')
    # 获取合约币种杠杆倍数 （5次/2s）
    # result = futureAPI.get_leverage('')
    # 设定合约币种杠杆倍数 （5次/2s）
    # 全仓
    # result = futureAPI.set_leverage('', '')
    # 逐仓
    # result = futureAPI.set_leverage('', '', '', '')
    # 账单流水查询 （5次/2s）
    # result = futureAPI.get_ledger('')
    # 下单 （60次/2s）
    # result = futureAPI.take_order('', '', '', '', client_oid='', order_type='0', match_price='0')

    # take orders
    # 批量下单 （30次/2s）
    # result = futureAPI.take_orders('', [
    #           {"client_oid": "", "type": "", "price": "", "size": "", "match_price": "0"},
    #           {"client_oid": "", "type": "", "price": "", "size": "", "match_price": "0"}
    # ])
    # 撤销指定订单 （40次/2s）
    # result = futureAPI.revoke_order('', '')
    # 批量撤销订单 （20次/2s）
    # result = futureAPI.revoke_orders('', client_oids=["", ""])
    # 获取订单列表 （10次/2s）
    # result = futureAPI.get_order_list('', '')
    # 获取订单信息 （60次/2s）
    # result = futureAPI.get_order_info('', '')
    # 获取成交明细 （10次/2s）
    # result = futureAPI.get_fills('')
    # 设置合约币种账户模式 （5次/2s）
    # result = futureAPI.set_margin_mode('', '')
    # 市价全平 （2次/2s）
    # result = futureAPI.close_position('', '')
    # 撤销所有平仓挂单 （5次/2s）
    # result = futureAPI.cancel_all('', '')
    # 获取合约挂单冻结数量 （5次/2s）
    # result = futureAPI.get_holds_amount('')
    # 委托策略下单 （40次/2s）
    # result = futureAPI.take_order_algo('', '', '', '', trigger_price='', algo_price='', algo_type='')
    # 委托策略撤单 （20次/2s）
    result = futureAPI.cancel_algos('BTC-USDT-200626', ['239946'], '1')
    # 获取委托单列表 （20次/2s）
    # result = futureAPI.get_order_algos('', '', status='')
    # 获取当前手续费费率 （1次/10s）
    # result = futureAPI.get_trade_fee()
    # 增加/减少保证金 （5次/2s）
    # result = futureAPI.change_margin('', '', '', '')
    # 设置逐仓自动增加保证金（5次/2s）
    #result = futureAPI.set_auto_margin('', '')
    # 公共-获取合约信息 （20次/2s）
    # result = futureAPI.get_products()
    # 公共-获取深度数据 （20次/2s）
    # result = futureAPI.get_depth('', '', '')
    # 公共-获取全部ticker信息 （20次/2s）
    # result = futureAPI.get_ticker()
    # 公共-获取某个ticker信息 （20次/2s）
    # result = futureAPI.get_specific_ticker('')
    # 公共-获取成交数据 （20次/2s）
    # result = futureAPI.get_trades('')
    # 公共-获取K线数据 （20次/2s）
    # result = futureAPI.get_kline('', '')
    # 公共-获取指数信息 （20次/2s）
    # result = futureAPI.get_index('')
    # 公共-获取法币汇率 （20次/2s）
    # result = futureAPI.get_rate()
    # 公共-获取预估交割价 （20次/2s）
    # result = futureAPI.get_estimated_price('')
    # 公共-获取平台总持仓量 （20次/2s）
    # result = futureAPI.get_holds('')
    # 公共-获取当前限价 （20次/2s）
    # result = futureAPI.get_limit('')
    # 公共-获取标记价格 （20次/2s）
    # result = futureAPI.get_mark_price('')
    # 公共-获取强平单 （20次/2s）
    # result = futureAPI.get_liquidation('', '')
    # 公共-获取历史结算/交割记录 （1次/60s）
    # result = futureAPI.get_history_settlement('')

# swap api test
# 永续合约API
    swapAPI = swap.SwapAPI(api_key, secret_key, passphrase, False)
    # 所有合约持仓信息 （1次/10s）
    # result = swapAPI.get_position()
    # 单个合约持仓信息 （20次/2s）
    # result = swapAPI.get_specific_position('')
    # 所有币种合约账户信息 （1次/10s）
    # result = swapAPI.get_accounts()
    # 单个币种合约账户信息 （20次/2s）
    # result = swapAPI.get_coin_account('')
    # 获取某个合约的用户配置 （5次/2s）
    # result = swapAPI.get_settings('')
    # 设定某个合约的杠杆 （5次/2s）
    # result = swapAPI.set_leverage('', '', '')
    # 账单流水查询 （5次/2s）
    # result = swapAPI.get_ledger('')
    # 下单 （40次/2s）
    # result = swapAPI.take_order('', '', '', '', order_type='0', client_oid='', match_price='0')
    # 批量下单 （20次/2s）
    # result = swapAPI.take_orders('', [
    #         {'client_oid': '', 'type': '', 'price': '', 'size': ''},
    #         {'client_oid': '', 'type': '', 'price': '', 'size': ''}
    #     ])
    # 撤单 （40次/2s）
    # result = swapAPI.revoke_order('', '')
    # 批量撤单 （20次/2s）
    # result = swapAPI.revoke_orders('', ids=['', ''])
    # 获取所有订单列表 （20次/2s）
    # result = swapAPI.get_order_list('', '')
    # 获取订单信息 （10次/2s）
    # result = swapAPI.get_order_info('', '')
    # 获取成交明细 （10次/2s）
    # result = swapAPI.get_fills('')
    # 获取合约挂单冻结数量 （5次/2s）
    # result = swapAPI.get_holds_amount('')
    # 委托策略下单 （40次/2s）
    # result = swapAPI.take_order_algo('', '', '', '', trigger_price='', algo_price='', algo_type='')
    # 委托策略撤单 （20 次/2s）
    # result = swapAPI.cancel_algos('', [''], '')
    # 获取委托单列表 （20次/2s）
    # result = swapAPI.get_order_algos('', '', algo_id='', status='')
    # 获取账户手续费费率 （5次/2s）
    # result = swapAPI.get_trade_fee()
    # 市价全平（2次/2s）
    # result = swapAPI.close_position('', '')
    # 撤销所有平仓挂单（5次/2s）
    # result = swapAPI.cancel_all('', '')
    # 公共-获取合约信息 （20次/2s）
    # result = swapAPI.get_instruments()
    # 公共-获取深度数据 （20次/2s）
    # result = swapAPI.get_depth('', '', '')
    # 公共-获取全部ticker信息 （20次/2s）
    # result = swapAPI.get_ticker()
    # 公共-获取某个ticker信息 （20次/2s）
    # result = swapAPI.get_specific_ticker('')
    # 公共-获取成交数据 （20次/2s）
    # result = swapAPI.get_trades('')
    # 公共-获取K线数据 （20次/2s）
    # result = swapAPI.get_kline('', '')
    # 公共-获取指数信息 （20次/2s）
    # result = swapAPI.get_index('')
    # 公共-获取法币汇率 （20次/2s）
    # result = swapAPI.get_rate()
    # 公共-获取平台总持仓量 （20次/2s）
    # result = swapAPI.get_holds('')
    # 公共-获取当前限价 （20次/2s）
    # result = swapAPI.get_limit('')
    # 公共-获取强平单 （20次/2s）
    # result = swapAPI.get_liquidation('', '')
    # 公共-获取合约资金费率 （20次/2s）
    # result = swapAPI.get_funding_time('')
    # 公共-获取合约标记价格 （20次/2s）
    # result = swapAPI.get_mark_price('')
    # 公共-获取合约历史资金费率 （20次/2s）
    # result = swapAPI.get_historical_funding_rate('')

# option api test
# 期权合约API
    optionAPI = option.OptionAPI(api_key, secret_key, passphrase, False)
    # 单个标的指数持仓信息 （20次/2s）
    # result = optionAPI.get_specific_position('')
    # 单个标的物账户信息 （20次/2s）
    # result = optionAPI.get_underlying_account('')
    # 下单 （20次/s）
    # result = optionAPI.take_order('', '', '', '', match_price='0')
    # 批量下单 （20次/2s）
    # result = optionAPI.take_orders('', [
    #         {"instrument_id": "", "side": "", "price": "", "size": "", "order_type": "0", "match_price": "0"},
    #         {"instrument_id": "", "side": "", "price": "", "size": "", "order_type": "0", "match_price": "0"}
    #     ])
    # 撤单 （20次/s）
    # result = optionAPI.revoke_order('', '')
    # 批量撤单 （20次/2s）
    # result = optionAPI.revoke_orders('', order_ids=["", ""])
    # 修改订单 （20次/s）
    # result = optionAPI.amend_order('', order_id='', new_price='', new_size='')
    # 批量修改订单 （20次/2s）
    # result = optionAPI.amend_batch_orders('', [
    #         {"order_id": "", "new_size": ""},
    #         {"client_oid": "", "request_id": "", "new_size": ""}
    #     ])
    # 获取单个订单状态 （40次/2s）
    # result = optionAPI.get_order_info('', '')
    # 获取订单列表 （10次/2s）
    # result = optionAPI.get_order_list('', '')
    # 获取成交明细 （10次/2s）
    # result = optionAPI.get_fills('')
    # 获取账单流水 （5次/2s）
    # result = optionAPI.get_ledger('')
    # 获取手续费费率 （1次/10s）
    # result = optionAPI.get_trade_fee()
    # 公共-获取标的指数 （20次/2s）
    # result = optionAPI.get_index()
    # 公共-获取期权合约 （20次/2s）
    # result = optionAPI.get_instruments('')
    # 公共-获取期权合约详细定价 （20次/2s）
    # result = optionAPI.get_instruments_summary('')
    # 公共-获取单个期权合约详细定价 （20次/2s）
    # result = optionAPI.get_option_instruments_summary('', '')
    # 公共-获取深度数据 （20次/2s）
    # result = optionAPI.get_depth('')
    # 公共-获取成交数据 （20次/2s）
    # result = optionAPI.get_trades('')
    # 公共-获取某个Ticker信息 （20次/2s）
    # result = optionAPI.get_specific_ticker('')
    # 公共-获取K线数据 （20次/2s）
    # result = optionAPI.get_kline('')

# index api test
# 指数API
    indexAPI = index.IndexAPI(api_key, secret_key, passphrase, False)
    # 公共-获取指数成分 （20次/2s）
    # result = indexAPI.get_index_constituents('')

# system api test
# 获取系统升级状态
    system = system.SystemAPI(api_key, secret_key, passphrase, False)
    # 公共-获取系统升级状态（1次/5s）
    # result = system.get_system_status('')


    print(time + json.dumps(result))