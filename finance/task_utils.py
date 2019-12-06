import json
import xml

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date
import timeit

# django setup
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'investment_portfolio.settings'
django.setup()

from finance.models import CurrentRate, HistoricalRate


def get_symbol(soup):
    name = soup.select(
        "#quote-header-info > div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1")[
        0].get_text()
    symbol = name.split()[0]
    return symbol


def get_current_rates(request):
    response = requests.get(request)
    current_status_dict = {}
    soup = BeautifulSoup(response.content, "html.parser")
    current_status_dict['symbol_id'] = get_symbol(soup)
    day_changes = soup.findAll("span", class_=["Trsdu(0.3s)"])
    current_status_dict['current_price'] = day_changes[0].get_text()
    day_change, day_change_percentage = day_changes[1].get_text().split(" ")
    current_status_dict['day_change'] = day_change
    current_status_dict['day_change_percentage'] = day_change_percentage[1:-2]
    return current_status_dict


def update_current_rate(current_status_dict):
    try:
        stock = CurrentRate.objects.get(symbol_id=current_status_dict['symbol_id'])
        stock.current_price = current_status_dict['current_price']
        stock.day_change = current_status_dict['day_change']
        stock.day_change_percentage = current_status_dict['day_change_percentage']
        stock.save()
    except ObjectDoesNotExist as e:
        CurrentRate.objects.create(**current_status_dict)


def get_historical_rates_webscraping(request):
    response = requests.get(request)
    soup = BeautifulSoup(response.content, "html.parser")
    table_data = soup.select("table")[0]
    symbol_id = get_symbol(soup)
    list_of_hist_rates = []
    # dict= {'symbol','date','open_price','high_price','low_price','close_price','adj_close_price','volume'}
    rows = table_data.select("tbody tr")
    for row in rows:
        list_of_spans = row.find_all('span')
        values = []
        dict = {}
        for span in list_of_spans:
            values.append(span.get_text())
        if values[1] != 'Dividend' and values[1] != 'Stock Split':  # todo stock splits
            dict['date'] = datetime.strptime(values[0], '%b %d, %Y')
            dict['open_price'] = values[1]
            dict['high_price'] = values[2]
            dict['low_price'] = values[3]
            dict['close_price'] = values[4]
            dict['adj_close_price'] = values[5]
            dict['symbol_id'] = symbol_id
            list_of_hist_rates.append(dict)
        elif values[1] == 'Dividend':
            dict['symbol_id'] = symbol_id
            dict['date'] = datetime.strptime(values[0], '%b %d, %Y')
            dict['dividend'] = values[1]
            dict['dividend_amount'] = row.find('strong').get_text()
    return list_of_hist_rates


# def update_historical_rates(list_of_hist_rates):
#     try:
#         last_update = HistoricalRate.objects.get(symbol_id=list_of_hist_rates[0]['symbol_id'])
#     except ObjectDoesNotExist as e:
#         for date_info in list_of_hist_rates:
#             if 'close_price' in date_info:
#                 HistoricalRate.objects.create(**date_info)

def update_historical_rates_bulk_insert(list_of_hist_rates):
    try:
        last_update = HistoricalRate.objects.get(symbol_id=list_of_hist_rates[0]['symbol_id'])
    except ObjectDoesNotExist as e:
        list_of_obj = []
        for date_info in list_of_hist_rates:
            if 'close_price' in date_info:
                obj = HistoricalRate(**date_info)
                list_of_obj.append(obj)
        HistoricalRate.objects.bulk_create(list_of_obj)


# update_current_rate(get_current_rates("https://finance.yahoo.com/quote/BND?p=BND&.tsrc=fin-srch"))
# update_current_rate(get_current_rates("https://finance.yahoo.com/quote/VOO?p=VOO&.tsrc=fin-srch"))
# hist_rates =get_historical_rates("https://finance.yahoo.com/quote/VOO/history?period1=1283979600&period2=1575583200&interval=1d&filter=history&frequency=1d")
# update_historical_rates_bulk_insert(hist_rates)
# HistoricalRate.objects.all().delete()
# def func_to_time():
#     update_historical_rates(hist_rates)
#     HistoricalRate.objects.all().delete()

# def func_to_time():
#     update_historical_rates_bulk_insert(hist_rates)
#     HistoricalRate.objects.all().delete()
# print(timeit.timeit(func_to_time, number=10))


def get_hist_data(request):
    response = requests.get(request)
    data = json.loads(response.text)
    list_of_hist_rates = []
    i=0
    for timestamp in data['chart']['result'][0]['timestamp']:
        dict = {}
        result_path = data['chart']['result'][0]
        path = result_path['indicators']['quote'][0]
        dict['date'] = datetime.fromtimestamp(timestamp).date()
        dict['open_price'] = path['open'][i]
        dict['high_price'] = path['high'][i]
        dict['low_price'] = path['low'][i]
        dict['close_price'] = path['close'][i]
        dict['adj_close_price'] = result_path['indicators']['adjclose'][0]['adjclose'][i]
        dict['symbol_id'] = result_path['meta']['symbol']
        list_of_hist_rates.append(dict)
        i += 1
    return list_of_hist_rates


def update_historical_dividends(request):
    response = requests.get(request)
    data = json.loads(response.text)
    for date in list((data['chart']['result'][0]['events']['dividends'].keys())):
        date_to_update = datetime.fromtimestamp(int(date)).date()
        obj = HistoricalRate.objects.get(date=date_to_update)
        obj.dividend_amount = data['chart']['result'][0]['events']['dividends'][date]['amount']
        obj.save() #todo bulk update


def func_to_time():
    request ="https://query2.finance.yahoo.com/v8/finance/chart/VTI?formatted=true&crumb=0ZXdu.gWVfg&lang=en-US&region=US&interval=1d&period1=992552400&period2=1575583200&events=div%7Csplit&corsDomain=finance.yahoo.com"
    HistoricalRate.objects.all().delete()
    update_historical_rates_bulk_insert(get_hist_data(request))
    update_historical_dividends(request)

func_to_time()

# for i, date in enumerate((data['chart']['result'][0]['events']['dividends'].keys())):
#     date_to_update = datetime.fromtimestamp(
#         int(list(data['chart']['result'][0]['events']['dividends'].keys())[i])).date()
#     obj = HistoricalRate.objects.get(date=date_to_update)
#     obj.dividend_amount = data['chart']['result'][0]['events']['dividends'][date]['amount']
#     obj.save()