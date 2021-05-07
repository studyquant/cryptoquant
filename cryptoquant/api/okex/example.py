import okex.account_api as account
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import json


if __name__ == '__main__':

    api_key = ""
    seceret_key = ""
    passphrase = ""

    # account api test
    accountAPI = account.AccountAPI(api_key, seceret_key, passphrase, True)
    # 钱包账户信息
    # result = accountAPI.get_wallet()
    # 单一币种账户信息
    # result = accountAPI.get_currency('usdt')
    # 资金划转`
    # result = accountAPI.coin_transfer('okb', '0.1','6','6','','')
    # 提币
    # result = accountAPI.coin_withdraw('eos','1','4','18339962991','123456',0)
    # 账单流水查询
    # result = accountAPI.get_ledger_record("","")
    # 获取充值地址
    # result = accountAPI.get_top_up_address('usdt')
    # 查询最近所有币种的提币记录
    # result = accountAPI.get_coins_withdraw_record()
    # 查询单个币种提币记录
    # result = accountAPI.get_coin_withdraw_record('BTC')
    # 获取所有币种充值记录
    # result = accountAPI.get_top_up_records()
    # 获取单个币种充值记录
    # result = accountAPI.get_top_up_record('BTC')
    # 获取币种列表
    # result = accountAPI.get_currencies()
    # 提币手续费
    # result = accountAPI.get_coin_fee('btc')



    # spot api test
    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
    # 币币账户信息
    # result = spotAPI.get_account_info()
    # 单一币种账户信息
    # result = spotAPI.get_coin_account_info('xrp')
    # 账单流水查询
    # result = spotAPI.get_ledger_record('usdt','21')
    # 下单
    # lient_oid, otype, side, instrument_id, order_type, price = '', size = '', notional = ''
    # result = spotAPI.take_order('','market','sell','BTC-USDT','0','9030','0.0075','')
    # 批量下单
    # params = [{"client_oid":"c123","instrument_id":"xrp-usdt","side":"sell","type":"limit","size":"1","price":"0.3"},
    #           {"client_oid":"d123","instrument_id":"xrp-usdt","side":"sell","type":"limit","size":"1","price":"0.3"}]
    # result = spotAPI.take_orders(params)
    # 撤销指定订单
    # result = spotAPI.revoke_order('3389267291932672','okb-usdt')
    # 批量撤销订单
    # result = spotAPI.revoke_orders([{'OKB-USDT',['3418277475195904','3418277475195905']},{'XRP-USDT',['3418281972599808','3418281972599809']}])
    # params=[{"instrument_id": "OKB-USDT", "order_ids": ['3418277475195904','3418277475195905']},
    #         {"instrument_id": "XRP-USDT", "order_ids": ['3418281972599808','3418281972599809']}]
    # result = spotAPI.revoke_orders(params)


    # 获取订单列表
    # result = spotAPI.get_orders_list('2','xrp-usdt','','',100)
    # 获取未成交订单
    # result = spotAPI.get_orders_pending()
    # 获取订单信息
    # result = spotAPI.get_order_info('3871608760253440','xrp-usdt')
    # 获取成交明细
    # result = spotAPI.get_fills('3871637364489216','XRP-USDT','')
    # 获取币对信息
    # result = spotAPI.get_coin_info()
    # 获取深度数据
    # result = spotAPI.get_depth('BTC-USDT','','0.1')
    # 获取全部ticker信息
    # result = spotAPI.get_ticker()
    # 获取某个ticker信息
    # result = spotAPI.get_specific_ticker('ABL-BTC')
    # 获取成交数据
    # result = spotAPI.get_deal('EOS-USDT','','','5')
    # 获取K线数据
    # result = spotAPI.get_kline('BTC-USDK',1800,'2019-11-13T08:00:00.000Z','2019-11-14T07:00:00.000Z')
    # 计划委托下单
    # result = spotAPI.order_algo('OKB-USDT','sell','1','1','1','3','2.99')
    # 跟踪委托下单
    # result = spotAPI.gzorder_algo('BTC-USD-SWAP','1','2','1','0.05','71610')
    # 冰山委托下单
    # result = spotAPI.bsorder_algo('BTC-USD-SWAP','1','2','1','0.05','71610','')
    # 时间加权下单
    # result = spotAPI.time_weighted('BTC-USD-SWAP', '1', '2', '1', '0.05', '71610')
    # 策略委托撤单
    # result = spotAPI.cancel_algos('OKB-USDT', ['314293'], '1')
    # 获取委托单列表
    # result = spotAPI.order_algo_list('OKB-USDT', '1', '','293678')

    # 获取指数成分
    # result = spotAPI.get_index('BTC-USD')


    # future api test
    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
    # 合约持仓信息
    # result = futureAPI.get_position()
    # 单个合约持仓信息
    # result = futureAPI.get_specific_position('XRP-USD-191101')
    # 所有币种合约账户信息
    # result = futureAPI.get_accounts()
    # 单个币种合约账户信息
    # result = futureAPI.get_coin_account('btc')
    # 获取合约币种杠杆倍数
    # result = futureAPI.get_leverage('btc-usd')
    # 设定合约币种杠杆倍数  全仓
    # result=futureAPI.set_leverage('eth',20)
    # 设定合约币种杠杆倍数  逐仓
    # result = futureAPI.set_leverage1('xrp-usd', 20, 'XRP-USD-191227', 'short')
    # 账单流水查询
    # result = futureAPI.get_ledger('ETH','','',100)
    # 下单
    # client_oid, instrument_id, otype, price, size,  leverage, order_type
    # result =futureAPI.take_order('a123', 'BTC-USD-191227', '3', '9250', '1', '15', '2')
    # 批量下单
    # orders = []
    # order2 = {"client_oid": "a123", "type": "1", "price": "0.01752", "size": "1", "match_price": "0",'order_type':'1'}
    # order3 = {"client_oid": "a234", "type": "1", "price": "0.01753", "size": "1", "match_price": "0",'order_type':'1'}
    # orders.append(order2)
    # orders.append(order3)
    # orders_data = json.dumps(orders)
    # # print(orders_data)
    # result = futureAPI.take_orders('TRX-USD-190927',  orders_data=orders_data)
    # 撤销指定订单
    # result = futureAPI.revoke_order('XRP-USD-191227','3712871667672064')
    # 批量撤单
    # result = futureAPI.revoke_orders('XRP-USD-191018',['3276121747110912','3276121750387712'])
    # 获取订单列表
    # result = futureAPI.get_order_list('2','','','100','BTC-USD-191227')
    # 获取订单信息
    # result = futureAPI.get_order_info('3819878650682369','XRP-USD-191227')
    # 获取成交明细
    # result = futureAPI.get_fills( '1870965382329344','EOS-USD-191227','','',100)
    # 设置合约币种账户模式
    # result=futureAPI.set_margin_mode('btc-usd','crossed')
    # 市价全平
    # result = futureAPI.close_position('EOS-USD-191227','long')
    # 撤销所有平仓挂单
    # result = futureAPI.cancel_all('EOS-USD-190927', 'long')
    # 获取合约信息接口
    # result = futureAPI.get_instruments()
    # 获取深度数据
    # result = futureAPI.get_depth('TRX-USD-191227', '','')
    # 获取全部ticker信息
    # result = futureAPI.get_ticker()
    # 获取某个ticker信息
    # result = futureAPI.get_specific_ticker('XRP-USD-190927')
    # 获取成交数据
    # result = futureAPI.get_trades('BTC-USD-190927',)
    # 获取k线数据
    # result = futureAPI.get_kline('ETH-USD-191227','900','2019-11-17T00:00:00.000Z','2019-11-18T00:00:00.000Z')
    # 获取指数信息
    # result = futureAPI.get_index('BTC-USD-190927')
    # 获取法币汇率
    # result = futureAPI.get_rate()
    # 获取预估交割价
    # result = futureAPI.get_estimated_price('BTC-USD-190927')
    # 获取平台总持仓量
    # result = futureAPI.get_holds('BTC-USD-190830')
    # 获取当前限价
    # result = futureAPI.get_limit('BTC-USD-190927')
    # 获取标记价格
    # result = futureAPI.mark_price('BTC-USD-191227')
    # 获取强平单
    # result = futureAPI.get_liquidation('BTC-USD-191227','1','','','')
    # 获取合约挂单冻结数量
    # result = futureAPI.get_holds_amount('EOS-USD-190927')
    # 计划委托下单
    # instrument_id, otype, order_type, size, trigger_price, algo_price
    # result = futureAPI.order_algo('XRP-USD-190927','1','1','1','0.2369','0.2368')
    # 跟踪委托下单
    # result = futureAPI.gzorder_algo('BTC-USD-SWAP','1','2','1','0.05','71610')
    # 冰山委托下单
    # result = futureAPI.bsorder_algo('BTC-USD-SWAP','1','2','1','0.05','71610','')
    # 时间加权下单
    # result = futureAPI.time_weighted('BTC-USD-SWAP', '1', '2', '1', '0.05', '71610')
    # 策略委托撤单
    # result = futureAPI.cancel_algos('XRP-USD-190927', '1877841,1877842', '1')
    # 获取委托单列表
    # result = futureAPI.order_algo_list('XRP-USD-191011', '1', '2','')



    # future api test 永续合约
    swapAPI = swap.SwapAPI(api_key, seceret_key, passphrase, True)
    # 获取所有合约持仓信息接口
    # result = swapAPI.get_position()
    # 单个合约持仓信息
    # result = swapAPI.get_specific_position('ETH-USD-SWAP')
    # 所有币种合约账户信息
    # result = swapAPI.get_accounts()
    # 某个币种合约账户信息
    # result = swapAPI.get_coin_account('BTC-USD-SWAP')
    # 获取某个合约的用户配置
    # result = swapAPI.get_leverage('BTC-USD-SWAP')
    # 设定某个合约的杠杆倍数
    # result = swapAPI.set_leverage('LTC-USD-SWAP','50','1')
    # 账单流水查询
    # result = swapAPI.get_ledger('BTC-USD-SWAP','','','','')
    # 下单
    # result = swapAPI.take_order('BTC-USD-SWAP','1','3500','1','0','1')
    # 批量下单
    # result = swapAPI.take_orders('BTC-USD-SWAP', [{"client_oid": "a11", "type": "1", "price": "10447", "size": '1', "match_price": "0"},
    #                                               {"client_oid": "b11", "type": "1", "price": "10446.9", "size": '1', "match_price": "0"}])

    # 撤销指定订单
    # result = swapAPI.revoke_order('BTC-USD-SWAP','291535374806097920')
    # 批量撤单
    # result = swapAPI.revoke_orders('BTC-USD-SWAP',['291655259563958272','291655259563958274'])
    # 获取订单列表
    # result = swapAPI.get_order_list('6', '330067407721148416', '', '100', 'ETH-USD-SWAP')
    # 获取订单信息
    # result = swapAPI.get_order_info('BTC-USD-SWAP','315454664070864896')
    # 获取成交明细
    # result = swapAPI.get_fills( '','BTC-USD-SWAP','','')
    # 获取合约信息
    # result = swapAPI.get_products()
    # 获取深度数据
    # result = swapAPI.get_depth('BTC-USDT-SWAP', 5)
    # 获取全部ticker信息
    # result = swapAPI.get_ticker()
    # 获取某个ticker信息
    # result = swapAPI.get_specific_ticker('BTC-USDT-SWAP')
    # 获取成交数据
    # result = swapAPI.get_trades('BTC-USDT-SWAP','','',100)
    # 获取合约k线
    # result = swapAPI.get_kline('BTC-USD-SWAP', '900', '', '')
    # 获取指数信息
    # result = swapAPI.get_index('BTC-USD-SWAP')
    # 获取法币汇率
    # result = swapAPI.get_rate()
    # 获取平台总持仓量
    # result = swapAPI.get_holds('BTC-USD-SWAP')
    # 获取当前限价
    # result = swapAPI.get_limit('BTC-USD-SWAP')
    # 获取强平单
    # result = swapAPI.get_liquidation('BTC-USDT-SWAP','1','','3','')
    # 获取合约挂单冻结数量
    # result = swapAPI.get_holds_amount('BTC-USD-SWAP')
    # 获取合约资金费率
    # result = swapAPI.get_close('BTC-USDT-SWAP')
    # 获取合约标记价格
    # result = swapAPI.get_tag_price('BTC-USDT-SWAP')
    # 获取合约历史资金费率
    # result = swapAPI.historical('BTC-USD-SWAP')
    # 计划委托下单
    # result = swapAPI.order_algo('BTC-USD-SWAP','1','1','1','8066.6','8066')
    # 跟踪委托下单
    # result = swapAPI.gzorder_algo('BTC-USD-SWAP','1','2','1','0.05','71610')
    # 冰山委托下单
    # result = swapAPI.bsorder_algo('BTC-USD-SWAP','1','2','1','0.05','71610','')
    # 时间加权下单
    # result = swapAPI.time_weighted('BTC-USD-SWAP', '1', '2', '1', '0.05', '71610')
    # 策略委托撤单
    # result = swapAPI.cancel_algos('BTC-USD-SWAP', ['332331187280748544'], '1')
    # 获取委托单列表
    # result = swapAPI.order_algo_list('BTC-USD-SWAP', '1', '','325633518317543424')



    # level api test
    levelAPI = lever.LeverAPI(api_key, seceret_key, passphrase, True)
    # 币币杠杆账户信息
    # result = levelAPI.get_account_info()
    # 单一币对账户信息
    # result = levelAPI.get_specific_account('eos-usdt')
    # 账单流水查询
    # result = levelAPI.get_ledger_record('xrp-usdt','', '','','')
    # 杠杆配置信息
    # result = levelAPI.get_config_info()
    # 某个杠杆配置信息
    # result = levelAPI.get_specific_config_info('ETH-USDT')
    # 获取借币记录
    # result = levelAPI.get_borrow_coin('1', '','','')
    # 某账户借币记录
    # result = levelAPI.get_specific_borrow_coin('EOS-USDT','1','','','')
    # 借币
    # result = levelAPI.borrow_coin('BTC-USDT','BTC','0.001')
    # 还币
    # result = levelAPI.repayment_coin('846888','BTC-USDT','BTC', '0.00100001')
    # 下单
    result = levelAPI.take_order('abc123456','limit', 'sell', 'TRX-USDT', '2', '10','0.2835')
    # 批量下单
    # params = [{"client_oid":"a2018","instrument_id":"TRX-USDT","side":"sell","type":"limit","size":"10","price":"0.2835","margin_trading":"2"},
    #          {"client_oid":"b2018","instrument_id":"TRX-USDT","side":"sell","type":"limit","size":"10","price":"0.2835","margin_trading":"2"}]
    # result = levelAPI.take_orders(params)
    # 撤销指定订单
    # result = levelAPI.revoke_order('3214806602027008','TRX-USDT')
    # 批量撤销订单
    # result = levelAPI.revoke_orders('TRX-USDT',['2856244929111040','2403463530818560'])
    # 获取订单列表
    # result = levelAPI.get_order_list('7','xrp-usdt','','','')
    # 获取订单信息
    # result = levelAPI.get_order_info('2578714163620864','xrp-usdt')
    # 获取所有未成交订单
    # result = levelAPI.get_order_pending()
    # 获取成交明细
    # result = levelAPI.get_fills('2403463530818560','XRP-USDT','','','')


    print(json.dumps(result))
