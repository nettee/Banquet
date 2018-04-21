#!/usr/bin/env python3

import re
import json

import requests

if __name__ == '__main__':

    for page_index in range(1, 5+1):

        data_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=hb&ft=&rs=&gs=0&sc=1nzf&st=desc&pi={}&pn=50&mg=a&dx=1'.format(page_index)

        res = requests.get(data_url)

        pattern = r'"(.*?)"'
        for m in re.finditer(pattern, res.text):
            print(m.group(1))


