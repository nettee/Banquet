#!/usr/bin/env python3

from datetime import date, datetime
import csv
import argparse

import numpy as np
import matplotlib.pyplot as plt

import fund
import stock

def stat(navs, prices, buys, subscription_rate=0.001):

    buy_dates, buy_values = zip(*buys)
    buy_value = sum(buy_values)

    shares = []

    print('共买入{}次，买入总金额¥{:.2f}元'.format(len(buy_values), buy_value))
    print('日期\t\t金额\t实际金额\t净值\t份额\t指数价格')
    for (bd, bv) in buys:
        rbv = bv - bv * subscription_rate
        nav = navs[bd]
        share = rbv / nav
        share = round(share, 2)
        price = prices[bd]
        print('{}\t¥{:.2f}\t¥{:.2f}\t\t{:.4f}\t{:.2f}\t{:.3f}'.format(bd, bv, rbv, nav, share, price[1]))

        shares.append(share)

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
    start_price = prices[start_date][1]

    all_data = []
    buy_data = []
    rel_price_data = []

    for (i, (dat, nav)) in enumerate(navs.items()):
        ratio = (nav - start_nav) / start_nav
        all_data.append((i, dat, nav, ratio))
        price = prices[dat][1]
        rel_price = price * start_nav / start_price
        rel_price_data.append((i, dat, rel_price))
        if dat in buy_dates:
            buy_data.append((i, dat, nav, ratio))

    i0, _, price = zip(*rel_price_data)
    plt.plot(i0, price, color='#CCCC00')

    i1, _, nav, _ = zip(*all_data)
    plt.plot(i1, nav, 'b')

    i2, _, nav2, _ = zip(*buy_data)
    plt.scatter(i2, nav2, color='#B22222')

    plt.hlines(cost, i1[0], i1[-1], color = 'c', linestyle = 'dashed')

    plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('code')
    parser.add_argument('index_code')
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

    navs = fund.nav(args.code, start_date)
    prices = stock.prices(args.index_code, start_date=start_date)
    stat(navs, prices, buys)
