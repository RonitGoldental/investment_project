import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist

# django setup
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'investment_portfolio.settings'
django.setup()

from finance.models import CurrentRate


def get_symbol(soup):
    name = soup.select(
        "#quote-header-info > div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1")[
        0].get_text()
    symbol = name.split()[0]
    return symbol


def task1(request):
    response = requests.get(request)
    soup = BeautifulSoup(response.content, "html.parser")
    table_data = soup.select("table")[0]  # todo check if there is more than one element
    symbol = get_symbol(soup)
    return (table_data, symbol)


def task2(table_data, symbol):
    list_of_dicts = []
    # dict= {'symbol','date','open_price','high_price','low_price','close_price','adj_close_price','volume'}
    rows = table_data.select("tbody tr")
    for row in rows:
        list_of_spans = row.find_all('span')
        values = []
        dict = {}
        for span in list_of_spans:
            values.append(span.get_text())
        if values[1] != 'Dividend' and values[1] != 'Stock Split':  # todo stock splits
            dict['date'] = values[0]
            dict['open_price'] = values[1]
            dict['high_price'] = values[2]
            dict['low_price'] = values[3]
            dict['close_price'] = values[4]
            dict['adj_close_price'] = values[5]
            dict['symbol'] = symbol
            list_of_dicts.append(dict)
        elif values[1] == 'Dividend':
            dict['date'] = values[0]
            dict['dividend'] = values[1]
            dict['dividend_amount'] = row.find('strong').get_text()
    return list_of_dicts


def task3(request):
    response = requests.get(request)
    current_status_dict = {}
    soup = BeautifulSoup(response.content, "html.parser")
    # current_status_dict['symbol'] = get_symbol(soup)
    day_changes = soup.findAll("span", class_=["Trsdu(0.3s)"])
    current_status_dict['current_price'] = day_changes[0].get_text()
    day_change, day_change_percentage = day_changes[1].get_text().split(" ")
    current_status_dict['day_change'] = day_change
    current_status_dict['day_change_percentage'] = day_change_percentage[1:-2]
    return current_status_dict


def update_current_rate(symbol,current_status_dict):
    try:
        obj = CurrentRate.objects.get(symbol=symbol)
    except ObjectDoesNotExist as e:
        CurrentRate.objects.create(symbol_id=symbol, **current_status_dict)
    obj = CurrentRate.objects.get(symbol=symbol)
    obj.current_price =current_status_dict['current_price']
    obj.day_change=current_status_dict['day_change']
    obj.day_change_percentage=current_status_dict['day_change_percentage']


# table_data,symbol = task1('https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI')
# list_of_dicts = task2(table_data,symbol)
# print(list_of_dicts)
# table_data,symbol = task1('https://finance.yahoo.com/quote/JPM/history?p=JPM')
# list_of_dicts = task2(table_data,symbol)
# print(list_of_dicts)
# table_data,symbol = task1('https://finance.yahoo.com/quote/NTZ/history?p=NTZ')
# list_of_dicts = task2(table_data,symbol)
# print(list_of_dicts)

update_current_rate('AA',task3("https://finance.yahoo.com/quote/VOO?p=VOO"))
print("end")
