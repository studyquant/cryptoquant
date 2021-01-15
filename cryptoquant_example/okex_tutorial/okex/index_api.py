from .client import Client
from .consts import *


class IndexAPI(Client):

    def __init__(self, api_key, api_secret_key, passphrase, use_server_time=False):
        Client.__init__(self, api_key, api_secret_key, passphrase, use_server_time)

    # get index constituents
    def get_index_constituents(self, instrument_id):
        return self._request_without_params(GET, INDEX_GET_CONSTITUENTS + str(instrument_id) + '/constituents')
