from webvpn import WebVPN
import nankaiLib as lib

vpn = WebVPN()
# log into webvpn
vpn.login('', '')
# init lib
vpn.get(lib.libic_url+lib.lib_webpage_uri)

# search by table name
date = "2022-01-05"
print(lib.searchByTab(vpn, table='F4B005', date=date, isAll=True))

# search by name
print(lib.searchByName(vpn, name='薛宇琼', date=date))
