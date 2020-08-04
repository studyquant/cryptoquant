# coding=utf-8
import json

class OkexAPIException(Exception):

    def __init__(self, response):
        self.code = 0
        try:
            json_res = response.json()
        except ValueError:
            self.message = 'Invalid JSON error message from Okex: {}'.format(response.text)
        else:
            if "code" in json_res.keys() and "message" in json_res.keys():
                self.code = json_res['code']
                self.message = json_res['message']
            elif "error_code" in json_res.keys() and "error_message" in json_res.keys():
                self.code = json_res['error_code']
                self.message = json_res['error_message']
            else:
                self.code = 'Please wait a moment'
                self.message = 'Maybe something is wrong'

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'API Request Error(code=%s): %s' % (self.code, self.message)


class OkexRequestException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'OkexRequestException: %s' % self.message


class OkexParamsException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'OkexParamsException: %s' % self.message
