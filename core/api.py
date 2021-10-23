import requests
import json
import urllib.parse
from requests.structures import CaseInsensitiveDict


class RequestsError(Exception):
    """Requests exception"""
    def __init__(self, reason, header=None, body=None):
        self.reason = str(reason)
        self.header = header
        self.body = body
        super(Exception, self).__init__(self, reason)

    def __str__(self):
        return self.reason


class Net:
    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        # self.requests = requests.Session()
        self.session = requests.session()  # fix due to #140
        self.additional_headers = CaseInsensitiveDict(
            requests_kwargs.pop('headers', {}))
        self.requests_kwargs = requests_kwargs

    def parse_json(self, value: str):
        return json.loads(value, object_hook=JsonDict)

    def requests_call(self,
                      method,
                      url,
                      headers=None,
                      params=None,
                      data=None,
                      stream=False):
        """ requests http/https call for Pixiv API """
        merged_headers = self.additional_headers.copy()
        if headers:
            # Use the headers in the parameter to override the
            # additional_headers setting.
            merged_headers.update(headers)
        if not merged_headers.get('User-Agent'):
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
            merged_headers['User-Agent'] = ua

        try:
            if method == 'GET':
                return self.session.get(url,
                                        params=params,
                                        headers=merged_headers,
                                        stream=stream,
                                        **self.requests_kwargs)
            elif method == 'POST':
                return self.session.post(url,
                                         params=params,
                                         data=data,
                                         headers=merged_headers,
                                         stream=stream,
                                         **self.requests_kwargs)
            elif method == 'DELETE':
                return self.session.delete(url,
                                           params=params,
                                           data=data,
                                           headers=merged_headers,
                                           stream=stream,
                                           **self.requests_kwargs)
        except Exception as e:
            raise RequestsError('requests %s %s error: %s' % (method, url, e))

        raise RequestsError('Unknown method: %s' % method)

    def unquote(self, html: str):
        return urllib.parse.unquote(html)


class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""
    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, attr, value):
        self[attr] = value
