#!/usr/bin/env python3

from datetime import datetime, timedelta

import requests
from sortedcontainers import SortedDict

url_template = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol={code}&period={period}&type=normal&begin={begin}&end={end}'

headers = {
        'Host': 'xueqiu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'Cookie': 'aliyungf_tc=AQAAAJxYPH6WkgsAuxiYJKhg/iIP2U7J; xq_a_token=0d524219cf0dd2d0a4d48f15e36f37ef9ebcbee1; xq_a_token.sig=P0rdE1K6FJmvC2XfH5vucrIHsnw; xq_r_token=7095ce0c820e0a53c304a6ead234a6c6eca38488; xq_r_token.sig=xBQzKLc4EP4eZvezKxqxXNtB7K0; u=431524363212524; device_id=93d87730caedd0cebd0615467104c660; __utma=1.221323187.1524363212.1524363212.1524363212.1; __utmb=1.6.10.1524363212; __utmc=1; __utmz=1.1524363212.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1524363213; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1524363695',
}

def xueqiu_timestamp(date):
    time = datetime(date.year, date.month, date.day)
    return round(time.timestamp() * 1000)

def prices(code, period='1day', start_date=None):

    if start_date is None:
        start_date = datetime.today() - timedelta(days=366)

    ps = SortedDict()

    url = url_template.format(code=code, period=period, begin=xueqiu_timestamp(start_date), end=xueqiu_timestamp(datetime.today()))
    res = requests.get(url, headers=headers)
    json = res.json()
    chartlist = json['chartlist']

    for chart in chartlist:
        timestamp = int(chart['timestamp']) / 1000
        date = datetime.fromtimestamp(timestamp).date()
        price = [float(chart[s]) for s in ('open', 'close', 'high', 'low')]
        ps[date] = price

    return ps

if __name__ == '__main__':

    code = 'SH000300'
    start_date = datetime(2018, 2, 1)
    stock(code, start_date=start_date)
