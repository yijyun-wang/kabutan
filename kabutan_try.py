# -*- coding: utf-8 -*-
# AUTHOR      : Yi-Jyun Wang

"""Try kabuta module.

Try kabuta module.

"""

from datetime import datetime as dt
import decimal
from decimal import Decimal
import kabutan

code_list = ['3903', '6753', '3076']
stock_dict = {}
for code in code_list:
    stock_dict[code] = {}
    print('getting stock (' + code + ') history ...')
    stock_dict[code]['history'] = kabutan.download_stock_history(code)
    stock_dict[code]['finance'] = kabutan.download_finance(code)

now_date = dt.now()

for code in code_list:
    # Calculate past per by past price.
    print('Stock ' + code + ' PER :')
    for i in range(2, 4):
        access_year = int(stock_dict[code]['finance'][i][0][:4])
        access_month = int(stock_dict[code]['finance'][i][0][-2:])
        stock_price_avg = kabutan.cal_month_avg(access_year, access_month,
                                                stock_dict[code]['history'])
        per = round(Decimal(stock_price_avg)
                    / Decimal(stock_dict[code]['finance'][i][5]), 2)
        print(stock_dict[code]['finance'][i][0]
              + " PER(past result) : "
              + str(stock_price_avg)
              + " / "
              + str(stock_dict[code]['finance'][i][5])
              + " = "
              + str(per))

    # Calculate last per by today's price.
    today_price = kabutan.fetch_today_price(code)
    try:
        per = round(Decimal(today_price)
                    / Decimal(stock_dict[code]['finance'][4][5]), 2)
        print(stock_dict[code]['finance'][4][0]
              + " PER(  predition) : "
              + str(today_price)
              + " / "
              + str(stock_dict[code]['finance'][4][5])
              + " = "
              + str(per))
    except decimal.InvalidOperation:
        print("There is no prediction.")
