#!/usr/bin/env python3

from datetime import date, datetime
import csv
import argparse

import numpy as np
import matplotlib.pyplot as plt

import nav

def stat(navs, buys, subscription_rate=0.001):

    buy_dates, buy_values = zip(*buys)
    buy_value = sum(buy_values)

    shares = []

    print('共买入{}次，买入总金额¥{:.2f}元'.format(len(buy_values), buy_value))
    print('日期\t\t金额\t实际金额\t净值\t份额')
    for (bd, bv) in buys:
        rbv = bv - bv * subscription_rate
        nav = navs[bd]
        share = rbv / nav
        share = round(share, 2)
        shares.append(share)
        print('{}\t¥{:.2f}\t¥{:.2f}\t\t{:.4f}\t{:.2f}'.format(bd, bv, rbv, nav, share))

    share = sum(shares)
    cost = buy_value / share
    print('持有份额：{:.2f}份，持仓成本价：{:.4f}'.format(share, cost))

    _, cnav = navs.peekitem(-1)
    cvalue = share * cnav
    print('当前金额：¥{:.2f}，当前净值：{:.4f}'.format(cvalue, cnav))

    holding_return = cvalue - buy_value
    holding_return_rate = holding_return / buy_value
    print('持有收益：¥{:.2f}，持有收益率：{:.2%}'.format(holding_return, holding_return_rate))

    start_date, start_nav = navs.peekitem(0)

    all_data = []
    buy_data = []

    for (i, (dat, nav)) in enumerate(navs.items()):
        ratio = (nav - start_nav) / start_nav
        all_data.append((i, dat, nav, ratio))
        if dat in buy_dates:
            buy_data.append((i, dat, nav, ratio))

    i, _, nav, _ = zip(*all_data)
    plt.plot(i, nav, 'b')

    i2, _, nav2, _ = zip(*buy_data)
    plt.scatter(i2, nav2, color='#B22222')

    plt.hlines(cost, i[0], i[-1], color = 'c', linestyle = 'dashed')

    plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('code')
    parser.add_argument('buy_file')

    args = parser.parse_args()

    buys = []

    with open(args.buy_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            bd, bv = row
            bd = datetime.strptime(bd, '%Y-%m-%d').date()
            bv = int(bv)
            buys.append((bd, bv))

    buy_dates, _ = zip(*buys)
    start_date = min(buy_dates)

    navs = nav.nav(args.code, start_date)
    stat(navs, buys)
