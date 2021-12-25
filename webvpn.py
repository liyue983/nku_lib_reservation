import requests
import re
import time
import base64
from hashlib import md5
from urllib.parse import urlparse
from Crypto.Cipher import AES

wrdvpnKey = 'wrdvpnisthebest!'
wrdvpnIV = 'wrdvpnisthebest!'

vpn_url = 'https://webvpn.nankai.edu.cn'
vpn_login_uri = '/login'

sso_url = 'https://sso.nankai.edu.cn'
sso_load_uri = '/sso/loadcode'
sso_login_uri = '/sso/login'


class WebVPN:
    def __init__(self, user=None, pasw=None) -> None:
        if user and pasw:
            self.login(user, pasw)

    def formVpnUrl(self, url):
        scheme = urlparse(url).scheme or 'http'
        return vpn_url + encrypUrl(scheme, url)

    def accountLogincode(self):
        sess = self.sess
        year = int(time.strftime("%Y", time.localtime()))
        time_stamp = int(time.time()*1000)
        s = str(year*time_stamp*33)+str(123)
        base = base64.b64encode(s.encode(encoding='UTF-8'))
        # load_url = 'https://webvpn.nankai.edu.cn/https/77726476706e69737468656265737421e3e44ed22931665b7f01c7a99c406d3635/sso/loadcode'
        load_url = self.formVpnUrl(sso_url + sso_load_uri)
        headers = {
            'Authorization': base,
            'X-Requested-With': 'XMLHttpRequest'
        }
        params = {
            "vpn-12-o2-sso.nankai.edu.cn": ""
        }
        data = sess.post(load_url, headers=headers, params=params)
        return data.json()['rand']

    def loginTicket(self, user, pasw, rand, lt):
        sess = self.sess
        md5_pasw = md5(pasw.encode(encoding='UTF-8')).hexdigest()
        # url = 'https://webvpn.nankai.edu.cn/https/77726476706e69737468656265737421e3e44ed22931665b7f01c7a99c406d3635/sso/login'
        url = self.formVpnUrl(sso_url+sso_login_uri)
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'}
        payload = {
            'ajax': '1',
            'username': str(user),
            'password': md5_pasw,
            'lt': lt,
            'rand': rand,
            # https://webvpn.nankai.edu.cn/login?cas_login=true'
            'service': vpn_url+'/login?cas_login=true',
            'loginType': '0'
        }
        params = {
            "vpn-12-o2-sso.nankai.edu.cn": ""
        }
        data = sess.post(url, data=payload, headers=headers,
                         params=params).json()
        if data['status']:
            print('登录成功...')
            return data['message']
        else:
            print('登录失败...')

    def login(self, user, pasw):
        self.sess = requests.session()
        sess = self.sess
        a = sess.get(vpn_url)
        lt = re.findall(' _lt = "(.*?)"', a.content.decode('UTF-8'))[0]
        rand = self.accountLogincode()
        ticket = self.loginTicket(user, pasw, rand, lt)
        params = {
            "cas_login": "true",
            "ticket": ticket
        }
        web_vpn_login_url = self.formVpnUrl(vpn_url + '/login')
        # 'https://webvpn.nankai.edu.cn/https/77726476706e69737468656265737421e7f2438a373e265e7f0682ad911b263174f121ab/login'
        sess.get(web_vpn_login_url, params=params)

    def get(self, url, **params):
        url_in_vpn = self.formVpnUrl(url)
        return self.sess.get(url_in_vpn, **params)

    def post(self, url, **params):
        url_in_vpn = self.formVpnUrl(url)
        return self.sess.post(url_in_vpn, **params)

    def request(self, method, url, **params):
        url_in_vpn = self.formVpnUrl(url)
        return self.sess.request(method, url_in_vpn, **params)


def encrypUrl(protocol, url):
    port = ""
    segments = ""

    if url[:7] == "http://":
        url = url[7:]
    elif url[:8] == "https://":
        url = url[8:]

    v6 = ""
    match = re.compile("/\[[0-9a-fA-F:]+?\]/").match(url)
    if match:
        v6 = match[0]
        url = url[len(match[0]):]
    segments = url.split("?")[0].split(":")
    if len(segments) > 1:
        port = segments[1].split("/")[0]
        url = url[0:len(segments[0])] + url[len(segments[0]) + len(port) + 1:]

    if protocol != "connection":
        i = url.find('/')
        if i == -1:
            if v6 != "":
                url = v6
            url = encrypt(url, wrdvpnKey, wrdvpnIV)
        else:
            host = url[:i]
            path = url[i:]
            if v6 != "":
                host = v6
            url = encrypt(host, wrdvpnKey, wrdvpnIV) + path
    if port != "":
        url = "/" + protocol + "-" + port + "/" + url
    else:
        url = "/" + protocol + "/" + url
    return url


def encrypt(text, key, iv):
    textLength = len(text)
    text = textRightAppend(text, 'utf8')
    keyBytes = key.encode(encoding='UTF-8')
    ivBytes = iv.encode(encoding='UTF-8')
    textBytes = text.encode(encoding='UTF-8')
    aesCfb = AES.new(keyBytes, AES.MODE_CFB, ivBytes, segment_size=128)
    encryptBytes = aesCfb.encrypt(textBytes)
    return ivBytes.hex() + encryptBytes.hex()[:textLength * 2]


def textRightAppend(text, mode):
    segmentByteSize = 16 if mode == 'utf8' else 32
    if len(text) % segmentByteSize == 0:
        return text
    appendLength = segmentByteSize - len(text) % segmentByteSize
    text += '0' * appendLength
    return text
