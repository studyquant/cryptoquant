from .client import Client
from .consts import *


class EttAPI(Client):

    def __init__(self, api_key, api_seceret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_seceret_key, passphrase, use_server_time)

    # query accounts
    def get_accounts(self):
        return self._request_without_params(GET, ETT_ACCOUNTS)

    # query account
    def get_account(self, symbol):
        return self._request_without_params(GET, ETT_ACCOUNT + str(symbol))

    # query ett ledger
    def get_ledger(self, symbol):
        return self._request_without_params(GET, ETT_LEDGER + str(symbol) + '/ledger')

    # take order
    def take_order(self, otype, quoto_currency, amount, size, ett, client_oid=''):
        params = {'type': otype, 'quoto_currency': quoto_currency, 'amount': amount, 'size': size, 'ett': ett, 'client_oid': client_oid}
        return self._request_with_params(POST, ETT_ORDER, params)

    # revoke order
    def revoke_order(self, order_id):
        return self._request_without_params(DELETE, ETT_REVOKE + str(order_id))

    # query order list
    #def get_order_list(self, status, ett, otype, before, after, limit):
    #    params = {'status': status, 'ett': ett, 'tyoe': otype, 'before': before, 'after': after, 'limit': limit}
    #    return self._request_with_params(GET, ETT_ORDER_LIST, params, cursor=True)

    def get_order_list(self, status, ett, otype, froms, to, limit):
        params = {'status': status, 'ett': ett, 'type': otype, 'from': froms, 'to': to, 'limit': limit}
        return self._request_with_params(GET, ETT_ORDER_LIST, params, cursor=True)

    # query order by id
    def get_specific_order(self, order_id):
        return self._request_without_params(GET, ETT_SPECIFIC_ORDER + str(order_id))

    # query ett constituents
    def get_constituents(self, ett):
        return self._request_without_params(GET, ETT_CONSTITUENTS + str(ett))

    # query ett define price
    def get_define_price(self, ett):
        return self._request_without_params(GET, ETT_DEFINE + str(ett))
