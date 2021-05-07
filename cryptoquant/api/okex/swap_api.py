from .client import Client
from .consts import *


class SwapAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False, first=False):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time, first)

    def get_position(self):
        return self._request_without_params(GET, SWAP_POSITIONS)

    def get_specific_position(self, instrument_id):
        return self._request_without_params(GET, SWAP_POSITION + str(instrument_id) + '/position')

    def get_accounts(self):
        return self._request_without_params(GET, SWAP_ACCOUNTS)

    def get_coin_account(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNT + str(instrument_id) + '/accounts')

    def get_settings(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNTS + '/' + str(instrument_id) + '/settings')

    def set_leverage(self, instrument_id, leverage, side):
        params = {'leverage': leverage, 'side': side}
        return self._request_with_params(POST, SWAP_ACCOUNTS + '/' + str(instrument_id) + '/leverage', params)

    def get_ledger(self, instrument_id, after='', before='', limit='', type=''):
        params = {}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        if type:
            params['type'] = type
        return self._request_with_params(GET, SWAP_ACCOUNTS + '/' + str(instrument_id) + '/ledger', params, cursor=True)

    def take_order(self, instrument_id, type, price, size, client_oid='', order_type='0', match_price=''):
        params = {'instrument_id': instrument_id, 'type': type, 'size': size, 'price': price}
        if client_oid:
            params['client_oid'] = client_oid
        if order_type:
            params['order_type'] = order_type
        if match_price:
            params['match_price'] = match_price
        return self._request_with_params(POST, SWAP_ORDER, params)

    def take_orders(self, instrument_id, order_data):
        params = {'instrument_id': instrument_id, 'order_data': order_data}
        return self._request_with_params(POST, SWAP_ORDERS, params)

    def revoke_order(self, instrument_id, order_id='', client_oid=''):
        if order_id:
            return self._request_without_params(POST, SWAP_CANCEL_ORDER + str(instrument_id) + '/' + str(order_id))
        elif client_oid:
            return self._request_without_params(POST, SWAP_CANCEL_ORDER + str(instrument_id) + '/' + str(client_oid))

    def revoke_orders(self, instrument_id, ids='', client_oids=''):
        params = {}
        if ids:
            params = {'ids': ids}
        elif client_oids:
            params = {'client_oids': client_oids}
        return self._request_with_params(POST, SWAP_CANCEL_ORDERS + str(instrument_id), params)

    def get_order_list(self, instrument_id, state, after='', before='', limit=''):
        params = {'state': state}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_ORDERS + '/' + str(instrument_id), params, cursor=True)

    def get_order_info(self, instrument_id, order_id='', client_oid=''):
        if order_id:
            return self._request_without_params(GET, SWAP_ORDERS + '/' + str(instrument_id) + '/' + str(order_id))
        elif client_oid:
            return self._request_without_params(GET, SWAP_ORDERS + '/' + str(instrument_id) + '/' + str(client_oid))

    def get_fills(self, instrument_id, order_id='', after='', before='', limit=''):
        params = {'instrument_id': instrument_id}
        if order_id:
            params['order_id'] = order_id
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_FILLS, params, cursor=True)

    def get_instruments(self):
        return self._request_without_params(GET, SWAP_INSTRUMENTS)

    def get_depth(self, instrument_id, size='', depth=''):
        params = {}
        if size:
            params['size'] = size
        if depth:
            params['depth'] = depth
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/depth', params)

    def get_ticker(self):
        return self._request_without_params(GET, SWAP_TICKETS)

    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/ticker')

    def get_trades(self, instrument_id, after='', before='', limit=''):
        params = {}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/trades', params, cursor=True)

    def get_kline(self, instrument_id, granularity='', start='', end=''):
        params = {}
        if granularity:
            params['granularity'] = granularity
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        # 按时间倒叙 即由结束时间到开始时间
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/candles', params)

        # 按时间正序 即由开始时间到结束时间
        # data = self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/candles', params)
        # return list(reversed(data))

    def get_index(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/index')

    def get_rate(self):
        return self._request_without_params(GET, SWAP_RATE)

    def get_holds(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/open_interest')

    def get_limit(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/price_limit')

    def get_liquidation(self, instrument_id, status, froms='', to='', limit=''):
        params = {'status': status}
        if froms:
            params['from'] = froms
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/liquidation', params)

    def get_holds_amount(self, instrument_id):
        return self._request_without_params(GET, SWAP_ACCOUNTS + '/' + str(instrument_id) + '/holds')

    # take order_algo
    def take_order_algo(self, instrument_id, type, order_type, size, trigger_price='', algo_price='',
                        callback_rate='', algo_variance='', avg_amount='', price_limit='', sweep_range='',
                        sweep_ratio='', single_limit='', time_interval=''):
        params = {'instrument_id': instrument_id, 'type': type, 'order_type': order_type, 'size': size}
        if order_type == '1':  # 止盈止损参数（最多同时存在10单）
            params['trigger_price'] = trigger_price
            params['algo_price'] = algo_price
        elif order_type == '2':  # 跟踪委托参数（最多同时存在10单）
            params['callback_rate'] = callback_rate
            params['trigger_price'] = trigger_price
        elif order_type == '3':  # 冰山委托参数（最多同时存在6单）
            params['algo_variance'] = algo_variance
            params['avg_amount'] = avg_amount
            params['price_limit'] = price_limit
        elif order_type == '4':  # 时间加权参数（最多同时存在6单）
            params['sweep_range'] = sweep_range
            params['sweep_ratio'] = sweep_ratio
            params['single_limit'] = single_limit
            params['price_limit'] = price_limit
            params['time_interval'] = time_interval
        return self._request_with_params(POST, SWAP_ORDER_ALGO, params)

    # cancel_algos
    def cancel_algos(self, instrument_id, algo_ids, order_type):
        params = {'instrument_id': instrument_id, 'algo_ids': algo_ids, 'order_type': order_type}
        return self._request_with_params(POST, SWAP_CANCEL_ALGOS, params)

    # get order_algos
    def get_order_algos(self, instrument_id, order_type, status='', algo_id='', before='', after='', limit=''):
        params = {'order_type': order_type}
        if status:
            params['status'] = status
        elif algo_id:
            params['algo_id'] = algo_id
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_GET_ORDER_ALGOS + str(instrument_id), params)

    # get_trade_fee
    def get_trade_fee(self):
        return self._request_without_params(GET, SWAP_GET_TRADE_FEE)

    def get_funding_time(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/funding_time')

    def get_mark_price(self, instrument_id):
        return self._request_without_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/mark_price')

    def get_historical_funding_rate(self, instrument_id, limit=''):
        params = {}
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/historical_funding_rate', params)
