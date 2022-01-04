# nku_lib_reservation

这个用来查询津南图书馆的座位信息、空闲座位、以及预定空闲座位。这里用到了之前写的一个工具[webvpn](https://github.com/liyue983/nankai-webvpn)，用来登录南开的 webvpn。

## 查询座位信息

[example1.py](example1.py)

```python
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
print(lib.searchByName(vpn, name='', date=date))

```

## 查询空闲座位

[example2.py](example2.py)

```python
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

# 查找指定时间空闲的座位，rooms可以为lib.rooms表示所有的区域，lib.rooms_most为3楼和4楼，或者自定义区域，比如rooms=['F4A','F4B']
r = lib.searchForAvailableByRequest(
    vpn, start=start, end=end, date=date, isAll=True, rooms=lib.rooms_most)

print(list([x['devName'] for x in r]))

```

## 预定空闲座位

[example3.py](eaxmple3.py)

<details>
<summary>前半部分代码与前面一致</summary>

```python
from webvpn import WebVPN
import nankaiLib as lib

vpn = WebVPN()
# log into webvpn
vpn.login('', '')
# init lib
vpn.get(lib.libic_url+lib.lib_webpage_uri)
```

</details>

```python
date = "2022-01-05"
start = "17:00"
end = "18:00"
rooms = ['F4A', 'F4B']

# 预定指定时间空闲的座位，retry为尝试次数，Center表示是否指定为中间的位置，rooms可以为lib.rooms表示所有的区域，lib。rooms_most为3楼和4楼，或者自定义区域，比如rooms=['F4A','F4B']
print(lib.reserveByNeeds(vpn, start=start, end=end, date=date,
                         rooms=rooms, retry=10, Center=False))

```

## 预定指定座位

[example4.py](eaxmple4.py)

<details>
<summary>前半部分代码与前面一致</summary>

```python
from webvpn import WebVPN
import nankaiLib as lib

vpn = WebVPN()
# log into webvpn
vpn.login('', '')
# init lib
vpn.get(lib.libic_url+lib.lib_webpage_uri)
```

</details>

```python
date = "2022-01-05"
start = "17:00"
end = "18:00"
tables = ['F4A054', 'F4B011']

# 根据tables尝试预定指定座位，retry为尝试次数。
lib.reserveByNeeds(vpn, start=start, end=end, date=date,
                   tables=tables, retry=10)
```
