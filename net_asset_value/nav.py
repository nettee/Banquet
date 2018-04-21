#!/usr/bin/env python3

from datetime import date, datetime
import re

import requests
from bs4 import BeautifulSoup
from sortedcontainers import SortedDict

url_template = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={code}&page={page}&per={per}'

def nav(code, start_date, target_dates=None):

    days = (date.today() - start_date).days

    url = url_template.format(code=code, page=1, per=days)

    res = requests.get(url)

    pattern = re.compile('<tr>.*?</tr>')
    lines = re.findall(pattern, res.text)
    lines.pop(0)

    navs = SortedDict()

    for line in lines:
        tr = BeautifulSoup(line, 'lxml')
        tds = tr.find_all('td')
        dat = datetime.strptime(tds[0].string, '%Y-%m-%d').date()
        if dat < start_date:
            continue
        if target_dates and dat not in target_dates:
            continue
        nav = float(tds[2].string)
        navs[dat] = nav

    return navs
