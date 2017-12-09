from httplib import OK as _HTTP_OK
from zlib import MAX_WBITS as _MAX_WBITS

from Cookie import CookieError
from httplib import HTTPException, BadStatusLine
from socket import error as SocketError

from Cookie import SimpleCookie
from decimal import Decimal
from hashlib import sha512 as _sha512
from hmac import new as newhash
from httplib import HTTPSConnection
from re import search
from urllib import urlencode
from zlib import decompress as _zdecompress

try:
    from simplejson import loads as jsonloads
except ImportError:
    from json import loads as jsonloads

COINONE_HOST = 'cryptottlivewebapi.xbtce.net'
API_REFRESH = 2            # data refresh time
CF_COOKIE = '__cfduid'     # CloudFlare security cookie
HTTP_TIMEOUT = 30          # connection timeout (max: 60 sec)

class APIError(Exception):
    "Raise exception when the BTC-e API returned an error."
    pass


class XBTCE(object):
    """BTC-e Trade/Public API persistent HTTPS connection.
    @cvar conn: shared httplib.HTTPSConnection between instances"""
    _headers = {         # common HTTPS headers
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'Accept-Encoding': 'gzip',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        }
    _post_headers = {    # common and POST headers
        'Content-Type': 'application/x-www-form-urlencoded',
        }
    conn = None    # type 'httplib.HTTPSConnection'
    resp = None    # type 'httplib.HTTPResponse'

    @classmethod
    def __init__(cls, compr=True, timeout=HTTP_TIMEOUT):
        """Initialization of shared HTTPS connection.
        @param compr: HTTPS compression (default: identity)
        @param timeout: HTTPS timeout (default/max: 30/60 sec)"""
        if compr is False:
            compr = 'identity'
        elif compr is True:
            compr = 'gzip, deflate'

        if not cls.conn:
            # Create a new connection.
            cls.conn = HTTPSConnection(COINONE_HOST,8443,strict=True, timeout=timeout)
            cls._post_headers.update(cls._headers)
        elif timeout != cls.conn.timeout:
            # Update the connection timeout.
            cls.conn.timeout = timeout
            cls.conn.close()
        if compr and compr != cls._headers['Accept-Encoding']:
            # Update the connection compression.
            cls._headers['Accept-Encoding'] = compr
            cls._post_headers.update(cls._headers)
            cls.conn.close()

    @classmethod
    def _signature(cls, apikey, msg):
        """Calculation of the SHA-512 authentication signature.
        @param apikey: API-key dict {'Key': '...', 'Secret': '...'}
        @param msg: method and parameters (Trade API)"""
        sign = newhash(apikey['Secret'], msg=msg, digestmod=_sha512)
        cls._post_headers['Key'] = apikey['Key']
        cls._post_headers['Sign'] = sign.hexdigest()

    @classmethod
    def _setcookie(cls):
        "Get the CloudFlare cookie and update security."
        cookie_header = cls.resp.getheader('Set-Cookie')
        try:
            cf_cookie = SimpleCookie(cookie_header)[CF_COOKIE]
        except (CookieError, KeyError):
            pass    # with/out previous cookie
        else:
            cf_value = cf_cookie.OutputString('value')
            cls._headers['Cookie'] = cls._post_headers['Cookie'] = cf_value

    @classmethod
    def _decompress(cls, data):
        """Decompress connection response.
        @return: decompressed data <type 'str'>"""
        encoding = cls.resp.getheader('Content-Encoding')
        if encoding == 'gzip':
            data = _zdecompress(data, _MAX_WBITS+16)
        elif encoding == 'deflate':
            data = _zdecompress(data, -_MAX_WBITS)
        # else: failback to 'identity' encoding
        return data

    @classmethod
    def jsonrequest(cls, url, apikey=None, **params):
        """Create query to the BTC-e API (JSON response).
        @raise httplib.HTTPException, socket.error: connection errors
        @param url: plain URL without parameters (Trade/Public API)
        @param apikey: API-key dict {'Key': '...', 'Secret': '...'}
        @param **params: method and/or parameters (Trade/Public API)
        @return: API response (JSON data) <type 'str'>"""
        if apikey:    # args: Trade API
            method = 'POST'
            body = urlencode(params)
            cls._signature(apikey, body)
            headers = cls._post_headers
        else:         # args: Public API
            method = 'GET'
            if params:
                url = '{}?{}'.format(url, urlencode(params))
            body = None
            headers = cls._headers
        while True:
            # Make a HTTPS request.
            try:
                cls.conn.request(method, url, body=body, headers=headers)
                cls.resp = cls.conn.getresponse()
            except BadStatusLine:
                cls.conn.close()
                continue
            except (HTTPException, SocketError):
                cls.conn.close()
                raise
            cls._setcookie()
            break
        return cls._decompress(cls.resp.read())

    @classmethod
    def apirequest(cls, url, apikey=None, **params):
        """Create query to the BTC-e API (decoded response).
        @raise APIError, httplib.HTTPException: BTC-e and CloudFlare errors
        @param url: plain URL without parameters (Public/Trade API)
        @param apikey: API-key dict {'Key': '...', 'Secret': '...'}
        @param **params: method and/or parameters (Public/Trade API)
        @return: API response (decoded data) <type 'dict'>"""
        data = cls.jsonrequest(url, apikey, **params)
        try:
            data = jsonloads(data, parse_float=Decimal, parse_int=Decimal)
        except ValueError:
            if cls.resp.status == _HTTP_OK:
                # BTC-e API unknown errors.
                raise APIError(str(data) or "Unknown Error")
            else:
                # HTTP or CloudFlare errors.
                raise HTTPException("{} {}".format(
                    cls.resp.status, cls.resp.reason))
        else:
            if 'error' in data:
                # BTC-e API standard errors.
                raise APIError(str(data['error']))
        return data

class PublicAPIv3(XBTCE):
    "BTC-e Public API v3 <https://btc-e.com/api/3/docs>."
    def __init__(self, *pairs, **connkw):
        """Initialization of the BTC-e Public API v3.
        @param *pairs: [btc_usd[-btc_rur[-...]]] or arguments
        @param **connkw: compr, timeout (see: BTCEConnection class)"""
        super(PublicAPIv3, self).__init__(**connkw)

        # Get and/or join all pairs.

    def call(self, method, pairs=None, **params):
        """Create query to the BTC-e Public API v3.
        @param method: info | ticker | depth | trades
        @param pairs: [btc_usd[-btc_rur[-...]]] <type 'str'>
        @param **params: limit=150 (max: 5000), ignore_invalid=1
        @return: API response (see: online documentation) <type 'dict'>"""
        url = '/api/v1/public/tick/{}'.format(method)
        return self.apirequest(url, **params)
