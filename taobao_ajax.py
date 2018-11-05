# _*_ coding: utf-8 _*_

import requests
import csv


keyword = '笔记本电脑'
offset = [x * 2 for x in range(1, 4)]

for num in offset:
    base_url = f'https://ai.taobao.com/search/getItem.htm?_tb_token_=e1bd07a39a6ae&__ajax__=1&page={num}&pageSize=60&key={keyword}'
    get_json = requests.get(base_url).json()
    get_info = get_json['result']['auction']
    products = []

    for info in get_info:
        description = info['description'].replace('&lt;span class=H&gt;', ',').replace('&lt;/span&gt;', ',').replace(';/span&gt;', ',').replace(',,', '')
        real_price = info['realPrice']
        sales_count = info['saleCount']
        product_link = info['picClickUrl']
        shop_name = info['nick']
        shop_location = info['itemLocation']
        products.append([description, real_price, sales_count, product_link, shop_name, shop_location])

    with open('test.csv', 'a', encoding='gbk', errors='ignore') as f:
        writer = csv.writer(f)
        writer.writerow(['宝贝名称', '价格', '销售数量', '宝贝链接', '店铺名称', '店铺所在地'])
        writer.writerows(products)

