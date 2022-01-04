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
rooms = ['F4A', 'F4B']

# 预定指定时间空闲的座位，retry为尝试次数，Center表示是否指定为中间的位置，rooms可以为lib.rooms表示所有的区域，lib。rooms_most为3楼和4楼，或者自定义区域，比如rooms=['F4A','F4B']
print(lib.reserveByNeeds(vpn, start=start, end=end, date=date,
                         rooms=rooms, retry=10, Center=False))
