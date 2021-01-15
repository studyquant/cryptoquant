from .client import Client
from .consts import *


class OptionAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time)

    def take_order(self, instrument_id, side, price, size, client_oid='', order_type='', match_price=''):
        params = {'instrument_id': instrument_id, 'side': side, 'price': price, 'size': size}
        if client_oid:
            params['client_oid'] = client_oid
        if order_type:
            params['order_type'] = order_type
        if match_price:
            params['match_price'] = match_price
        return self._request_with_params(POST, OPTION_ORDER, params)

    def take_orders(self, underlying, order_data):
        params = {'underlying': underlying, 'order_data': order_data}
        return self._request_with_params(POST, OPTION_ORDERS, params)

    def revoke_order(self, underlying, order_id='', client_oid=''):
        if order_id:
            return self._request_without_params(POST, OPTION_CANCEL_ORDER + str(underlying) + '/' + str(order_id))
        elif client_oid:
            return self._request_without_params(POST, OPTION_CANCEL_ORDER + str(underlying) + '/' + str(client_oid))

    def revoke_orders(self, underlying, order_ids='', client_oids=''):
        params = {}
        if order_ids:
            params = {'order_ids': order_ids}
        elif client_oids:
            params = {'client_oids': client_oids}
        return self._request_with_params(POST, OPTION_CANCEL_ORDERS + str(underlying), params)

    def amend_order(self, underlying, order_id='', client_oid='', request_id='', new_size='', new_price=''):
        params = {}
        if order_id:
            params['order_id'] = order_id
        elif client_oid:
            params['client_oid'] = client_oid
        if new_size:
            params['new_size'] = new_size
        if new_price:
            params['new_price'] = new_price
        if request_id:
            params['request_id'] = request_id
        return self._request_with_params(POST, OPTION_AMEND_ORDER + str(underlying), params)

    def amend_batch_orders(self, underlying, amend_data):
        params = {'amend_data': amend_data}
        return self._request_with_params(POST, OPTION_AMEND_BATCH_ORDERS + str(underlying), params)

    def get_order_info(self, underlying, order_id='', client_oid=''):
        if order_id:
            return self._request_without_params(GET, OPTION_ORDERS + '/' + str(underlying) + '/' + str(order_id))
        elif client_oid:
            return self._request_without_params(GET, OPTION_ORDERS + '/' + str(underlying) + '/' + str(client_oid))

    def get_order_list(self, underlying, state, instrument_id='', after='', before='', limit=''):
        params = {'state': state}
        if instrument_id:
            params['instrument_id'] = instrument_id
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, OPTION_ORDERS + '/' + str(underlying), params, cursor=True)

    def get_fills(self, underlying, order_id='', instrument_id='', after='', before='', limit=''):
        params = {}
        if order_id:
            params['order_id'] = order_id
        if instrument_id:
            params['instrument_id'] = instrument_id
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, OPTION_FILLS + str(underlying), params, cursor=True)

    def get_specific_position(self, underlying, instrument_id=''):
        params = {}
        if instrument_id:
            params['instrument_id'] = instrument_id
        return self._request_with_params(GET, OPTION_POSITION + str(underlying) + '/position', params)

    def get_underlying_account(self, underlying):
        return self._request_without_params(GET, OPTION_ACCOUNT + str(underlying))

    def get_ledger(self, underlying, after='', before='', limit=''):
        params = {}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, OPTION_ACCOUNT + str(underlying) + '/ledger', params, cursor=True)

    def get_trade_fee(self):
        return self._request_without_params(GET, OPTION_TRADE_FEE)

    def get_index(self):
        return self._request_without_params(GET, OPTION_INDEX)

    def get_instruments(self, underlying, delivery='', instrument_id=''):
        params = {}
        if delivery:
            params['delivery'] = delivery
        if instrument_id:
            params['instrument_id'] = instrument_id
        return self._request_with_params(GET, OPTION_INSTRUMENTS + str(underlying), params)

    def get_instruments_summary(self, underlying, delivery=''):
        params = {}
        if delivery:
            params['delivery'] = delivery
        return self._request_with_params(GET, OPTION_INSTRUMENTS + str(underlying) + '/summary', params)

    def get_option_instruments_summary(self, underlying, instrument_id):
        return self._request_without_params(GET, OPTION_INSTRUMENTS + str(underlying) + '/summary/' + str(instrument_id))

    def get_depth(self, instrument_id, size=''):
        params = {}
        if size:
            params['size'] = size
        return self._request_with_params(GET, OPTION_INSTRUMENTS + str(instrument_id) + '/book', params)

    def get_trades(self, instrument_id, after='', before='', limit=''):
        params = {}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, OPTION_INSTRUMENTS + str(instrument_id) + '/trades', params, cursor=True)

    def get_specific_ticker(self, instrument_id):
        return self._request_without_params(GET, OPTION_INSTRUMENTS + str(instrument_id) + '/ticker')

    def get_kline(self, instrument_id, start='', end='', granularity=''):
        params = {}
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        if granularity:
            params['granularity'] = granularity
        # 按时间倒叙 即由结束时间到开始时间
        # return self._request_with_params(GET, OPTION_INSTRUMENTS + str(instrument_id) + '/candles', params)

        # 按时间正序 即由开始时间到结束时间
        data = self._request_with_params(GET, OPTION_INSTRUMENTS + str(instrument_id) + '/candles', params)
        return list(reversed(data))
