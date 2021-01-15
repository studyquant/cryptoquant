from .client import Client
from .consts import *


class LeverAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time)

    # query lever account info
    def get_account_info(self):
        return self._request_without_params(GET, LEVER_ACCOUNT)

    # query specific account info
    def get_specific_account(self, instrument_id):
        return self._request_without_params(GET, LEVER_COIN_ACCOUNT + str(instrument_id))

    # query ledger record
    def get_ledger_record(self, instrument_id, after='', before='', limit='', type=''):
        params = {}
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        if type:
            params['type'] = type
        return self._request_with_params(GET, LEVER_LEDGER_RECORD + str(instrument_id) + '/ledger', params, cursor=True)

    # query lever config info
    def get_config_info(self):
        return self._request_without_params(GET, LEVER_CONFIG)

    # query specific config info
    def get_specific_config_info(self, instrument_id):
        return self._request_without_params(GET, LEVER_SPECIFIC_CONFIG + str(instrument_id) + '/availability')

    def get_borrow_coin(self, status='', after='', before='', limit=''):
        params = {'status': status, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, LEVER_BORROW_RECORD, params, cursor=True)

    def get_specific_borrow_coin(self, instrument_id, status='', after='', before='', limit=''):
        params = {'status': status, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, LEVER_SPECIFIC_CONFIG + str(instrument_id) + '/borrowed', params, cursor=True)

    # borrow coin
    def borrow_coin(self, instrument_id, currency, amount):
        params = {'instrument_id': instrument_id, 'currency': currency, 'amount': amount}
        return self._request_with_params(POST, LEVER_BORROW_COIN, params)

    # repayment coin
    def repayment_coin(self, instrument_id, currency, amount, borrow_id=''):
        params = {'instrument_id': instrument_id, 'currency': currency, 'amount': amount}
        if borrow_id:
            params['borrow_id'] = borrow_id
        return self._request_with_params(POST, LEVER_REPAYMENT_COIN, params)

    # take order
    def take_order(self, instrument_id, side, margin_trading, client_oid='', type='', order_type='0', price='', size='', notional=''):
        params = {'instrument_id': instrument_id, 'side': side, 'margin_trading': margin_trading, 'client_oid': client_oid, 'type': type, 'order_type': order_type, 'price': price, 'size': size, 'notional': notional}
        return self._request_with_params(POST, LEVER_ORDER, params)

    def take_orders(self, params):
        return self._request_with_params(POST, LEVER_ORDERS, params)

    # revoke order
    def revoke_order(self, instrument_id, order_id='', client_oid=''):
        params = {'instrument_id': instrument_id}
        if order_id:
            return self._request_with_params(POST, LEVER_REVOKE_ORDER + str(order_id), params)
        elif client_oid:
            return self._request_with_params(POST, LEVER_REVOKE_ORDER + str(client_oid), params)

    def revoke_orders(self, params):
        return self._request_with_params(POST, LEVER_REVOKE_ORDERS, params)

    # query order list
    def get_order_list(self, instrument_id, state, after='', before='', limit=''):
        params = {'instrument_id': instrument_id, 'state': state, 'after': after, 'before': before, 'limit': limit}
        return self._request_with_params(GET, LEVER_ORDER_LIST, params, cursor=True)

    def get_order_pending(self, instrument_id, after='', to='', limit=''):
        params = {'instrument_id': instrument_id}
        if after:
            params['after'] = after
        if to:
            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, LEVEL_ORDERS_PENDING, params, cursor=True)

    # query order info
    def get_order_info(self, instrument_id, order_id='', client_oid=''):
        params = {'instrument_id': instrument_id}
        if order_id:
            return self._request_with_params(GET, LEVER_ORDER_INFO + str(order_id), params)
        elif client_oid:
            return self._request_with_params(GET, LEVER_ORDER_INFO + str(client_oid), params)

    def get_fills(self, instrument_id, order_id='', after='', to='', limit=''):
        params = {'instrument_id': instrument_id, 'order_id': order_id, 'after': after, 'to': to, 'limit': limit}
        return self._request_with_params(GET, LEVER_FILLS, params, cursor=True)

    def get_leverage(self, instrument_id):
        return self._request_without_params(GET, LEVER_LEDGER_RECORD + str(instrument_id) + '/leverage')

    def set_leverage(self, instrument_id, leverage):
        params = {'leverage': leverage}
        return self._request_with_params(POST, LEVER_LEDGER_RECORD + str(instrument_id) + '/leverage', params)

    def get_mark_price(self, instrument_id):
        return self._request_without_params(GET, LEVER_MARK_PRICE + str(instrument_id) + '/mark_price')
