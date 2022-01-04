#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
# from webvpn import WebVPN


# In[2]:


# vpn = WebVPN()


# In[3]:


libic_url = 'https://libic.nankai.edu.cn'
rsv_state_uri = '/ClientWeb/pro/ajax/device.aspx'
set_rsv_uri = '/ClientWeb/pro/ajax/reserve.aspx'
lib_webpage_uri = '/clientweb/xcus/ic2/Default.aspx'

# In[4]:


def get_rsv_state(sess, room_id='', date=None, classkind=8, act='get_rsv_sta', start=None, end=None):
    date = datetime.date.today() if not date else date
    params = {
        "byType": "devcls",
        "classkind": classkind,
        "date": date,
        "act": act,
        "room_id": room_id
    }
    if start and end:
        params["fr_start"] = start
        params["fr_end"] = end
    url = libic_url+rsv_state_uri
    a = sess.get(url, params=params)
    return a.json()['data']


# In[5]:


def get_rm_state(sess, date=None, classkind=8, act='get_rsv_sta'):
    date = datetime.date.today() if not date else date
    params = {
        "byType": "devcls",
        "classkind": classkind,
        "date": date,
        "act": act,
    }
    url = libic_url + rsv_state_uri
    a = sess.get(url, params=params)
    return a.json()['data']


# In[6]:


def get_one_table():
    # TODO or Not Userful
    # https://libic.nankai.edu.cn/ClientWeb/pro/ajax/device.aspx?date=20211225&classkind=8&dev_id=919925&act=get_rsv_sta&_nocache=1640399292619
    result = []
    params = {
        "data": 20211225,
        "clsskind": 8,
        "dev_id": 919925,
        "act": "get_rsv_sta"
    }
    pass


# In[7]:


room_ids = {'F3A': '837656', 'F3B': '837668', 'F3C': '837677', 'F3D': '837686', 'F3E': '837699', 'F3F': '837708', 'F3G': '837738', 'F3V': '837745', 'F4A': '838370', 'F4B': '838372', 'F4C': '838375', 'F4D': '838377',
            'F4E': '838379', 'F4F': '838383', 'F4G1': '838385', 'F4G2': '838387', 'F4V': '838389', 'F5A': '838393', 'F5B': '838395', 'F5G': '838397', 'F5V': '838399', 'F7A': '838401', 'F7B': '838404', 'F7C': '838407', 'F7D': '838409'}


# In[8]:


def searchByName(sess, name='', date=None, isAll=False):
    result = []
    for room_id in room_ids.values():
        sectionJson = get_rsv_state(sess, room_id=room_id, date=date)
        for tab in sectionJson:
            for us in tab['ts']:
                if us['owner'] == name:
                    temp = {
                        "devName": tab['devName'],
                        "owner": us['owner'],
                        "start": us['start'],
                        "end": us['end'],
                        "state": us['state']
                    }
                    result.append(temp)
                    # print(result)
                    if not isAll:
                        return result
    return result


# In[9]:


def searchByTab(sess, table='F4E017', date=None, isAll=False):
    result = []
    table = table.upper()
    room_id = room_ids[table[:3]]
    sectionJson = get_rsv_state(sess, room_id=room_id, date=date)
    for tab in sectionJson:
        if tab['title'] == table:
            for us in tab['ts']:
                temp = {
                    "devName": tab['devName'],
                    "owner": us['owner'],
                    "start": us['start'],
                    "end": us['end'],
                    "state": us['state']
                }
                result.append(temp)
                if not isAll:
                    return result
            return result
    return result


# In[10]:


def searchForAvailableByRequest(sess, start, end, date=None, isAll=True, rooms=None):
    result = []
    rooms = rooms or room_ids.keys()
    for room_name in rooms:
        room_id = room_ids[room_name]
        sectionJson = get_rsv_state(
            sess, room_id=room_id, date=date, start=start, end=end)
        if sectionJson is None:
            continue
        for tab in sectionJson:
            if tab["state"] != "close" and tab["freeSta"] == 0:
                result.append(tab)
                if not isAll:
                    return result
    return result


# In[11]:


def getTabInfByTabname(sess, table='F4E017', date=None):
    table = table.upper()
    room_id = room_ids[table[:3]]
    sectionJson = get_rsv_state(sess, room_id=room_id, date=date)
    for tab in sectionJson:
        if tab['title'] == table:
            return tab


# In[12]:


def setReserve(sess, table="F4E023", tableInf=None, start=None, end=None):
    tabInf = tableInf or getTabInfByTabname(sess, table)
    params = {
        'dev_id': tabInf['devId'],
        'lab_id': tabInf['labId'],
        'room_id': tabInf['roomId'],
        'kind_id': tabInf['kindId'],
        'type': 'dev',
        'classkind': 8,
        'start': start,  # '2021-12-25 11:30',
        'end': end,  # 2021-12-25 14:00',
        'act': 'set_resv'
    }
    url = libic_url + set_rsv_uri
    a = sess.get(url, params=params)
    return a.json()


# In[13]:


def reserveByNeeds(sess, start, end, date=None, rooms=[], tables=[], retry=1, Center=False):
    date = date or str(datetime.date.today())
    rooms_in_tables = list(set([x[:3] for x in tables]))
    rooms = rooms_in_tables or rooms or room_ids.keys()
    print(rooms)
    for i in range(retry):
        for room_name in rooms:
            room_id = room_ids[room_name]
            sectionJson = get_rsv_state(
                sess, room_id=room_id, date=date, start=start, end=end)
            if sectionJson is None:
                continue
            for tab in sectionJson:
                if tab["state"] != "close" and tab["freeSta"] == 0:
                    if tables and (tab['devName'] not in tables):
                        continue
                    if Center:
                        tabind = int(tab['devName'][-3:])
                        if tabind <= len(sectionJson)/2 and (tabind-5) % 6 != 0:
                            continue
                        elif tabind > len(sectionJson)/2 and (tabind-2) % 6 != 0:
                            continue
                    print(tab['devName'])
                    set_result = setReserve(
                        sess, tableInf=tab, start=date+" "+start, end=date+" "+end)
                    print(set_result)
                    if set_result['ret'] == 1:
                        return set_result
    print('没有符合的')
    return


# In[14]:


rooms_most = ['F3A', 'F3B', 'F3C', 'F3D', 'F3E', 'F3F',
              'F4A', 'F4B', 'F4C', 'F4D', 'F4E', 'F4F'][::-1]
rooms = ['F4B']
tables = ['F4B005', 'F4B011', 'F4B017', 'F4B023', 'F4B029', 'F4B035']


# In[15]:


date = "2021-12-29"
start = "08:30"
end = "23:00"


# In[16]:


if __name__ == '__main__':
    pass
    # vpn.login('', '')
    # # vpn.get(libic_url)
    # print(searchByTab(vpn,table='F4E017'))
    # print(searchForAvailableByRequest(vpn,start=start,end=end,date=date,isAll=True,rooms=rooms))
    # print(setReserve(vpn,table="F4E023",tableInf=None,start=start,end=end))
    # reserveByNeeds(vpn,start=start,end=end,date=date,rooms=rooms,retry=100)


# In[17]:


# 预定rooms中间的位置
# reserveByNeeds(vpn, start=start, end=end, date=date,
#                rooms=rooms, retry=1, Center=True)


# In[18]:


# reserveByNeeds(vpn,start=start,end=end,date=date,rooms=rooms_most,retry=100)


# In[19]:


# 预定tables
# reserveByNeeds(vpn,start=start,end=end,date=date,tables=tables,retry=10)
