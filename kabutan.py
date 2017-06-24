# -*- coding: utf-8 -*-
# AUTHOR      : Yi-Jyun Wang

"""kabutan.com. web scraping module.

Download stock tables from kabutan.com. such as:
 - Time series table of stock price
 - Progress against the expected eps ranking table
 - Past performance table

"""

from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def get_item(stock_bsObj):
    """Parse <tr> tag to get all item in it."""
    item_list = []
    for item in stock_bsObj.children:
        if(item == '\n'):
            continue
        else:
            #
            if(re.compile('[0-9]{2}/[0-9]{2}').match(item.string)):
                item_list.append('20'+item.string)
            else:
                item_list.append(str(item.string).replace(",", ""))
    return item_list


def download_stock_history(code):
    """Download time series table of stock cade {code}."""
    stock_ts = []
    for page in range(1, 11):
        site_url = 'https://kabutan.jp/stock/kabuka?code='\
                    + code + '&ashi=wek&page=' + str(page)
        html = urlopen(site_url)
        html_bsObj = BeautifulSoup(html, "html.parser")
        for sibling in html_bsObj.find("table",
                                       {"class": "stock_kabuka2"}
                                       ).tr.next_siblings:
            if(sibling == '\n'):
                continue
            else:
                stock_ts.append(get_item(sibling))
    return stock_ts


def cal_month_avg(year, month, stock_ts):
    """Calculate stock price average in specified month."""
    value = []
    for week in stock_ts:
        date = datetime.strptime(week[0], '%Y/%m/%d')
        if(date.year == year and date.month == month):
            value.append(int(week[4]))
    try:
        return sum(value)/len(value)
    except ZeroDivisionError:
        return 'Data not found.'


def download_finance(code):
    """Download past finance table of stock code {code}."""
    stock_finance_table = []
    tag_list = []
    site_url = 'https://kabutan.jp/stock/finance?code=' + code
    html = urlopen(site_url)
    html_bsObj = BeautifulSoup(html, "html.parser")
    for tr_tag in html_bsObj.find("div", {"id": "finance_box"}).table.children:
        tag_list.append(tr_tag)
    for i in range(5, 14, 2):
        year_fin_list = []
        year_fin_list.append(tag_list[i].td.text[-7:])
        for td_tag in tag_list[i].td.next_siblings:
            try:
                year_fin_list.append(td_tag.text)
            except AttributeError:
                continue
        stock_finance_table.append(year_fin_list)

    return stock_finance_table


def fetch_today_price(code):
    """Fetch last price of stock code {code} from kabutan."""
    site_url = 'https://kabutan.jp/stock/kabuka?code=' + code
    html = urlopen(site_url)
    html_bsObj = BeautifulSoup(html, "html.parser")
    tr_tag = html_bsObj.find("table", {"class": "stock_kabuka0"}).tr
    price = tr_tag.next_sibling.next_sibling.td.next.next.next.text
    price = price.replace(",", "")
    return int(price)
