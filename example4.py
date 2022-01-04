from webvpn import WebVPN
import nankaiLib as lib

vpn = WebVPN()
# log into webvpn
vpn.login('', '')
# init lib
vpn.get(lib.libic_url+lib.lib_webpage_uri)

date = "2022-01-05"
start = "17:00"
end = "18:00"
tables = ['F4A054', 'F4B011']

# 根据tables尝试预定指定座位，retry为尝试次数。
lib.reserveByNeeds(vpn, start=start, end=end, date=date,
                   tables=tables, retry=10)
