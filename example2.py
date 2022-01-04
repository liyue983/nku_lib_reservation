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

# 查找指定时间空闲的座位，rooms可以为lib.rooms表示所有的区域，lib。rooms_most为3楼和4楼，或者自定义区域，比如rooms=['F4A','F4B']
r = lib.searchForAvailableByRequest(
    vpn, start=start, end=end, date=date, isAll=True, rooms=lib.rooms_most)

print(list([x['devName'] for x in r]))
