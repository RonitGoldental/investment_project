import json
import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
import datetime
import timeit

# django setup
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'investment_portfolio.settings'
django.setup()

from finance.models import CurrentRate, HistoricalRate, Stock


def get_symbol(soup):
    name = soup.select(
        "#quote-header-info > div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1")[
        0].get_text()
    symbol = name.split()[0]
    return symbol


def get_current_rates(request):
    response = requests.get(request)
    data = json.loads(response.text)
    current_status_dict = {}
    # current_status_dict['symbol_id']
    # current_status_dict['time_updated']
    # current_status_dict['current_price'] =
    # current_status_dict['day_change'] =
    # current_status_dict['day_change_percentage'] =
    return current_status_dict


def update_current_rate(current_status_dict):
    obj, created = CurrentRate.objects.update_or_create(symbol_id=current_status_dict['symbol_id'],defaults=current_status_dict)
    # try:
    #     stock = CurrentRate.objects.get(symbol_id=current_status_dict['symbol_id'])
    #     stock.current_price = current_status_dict['current_price']
    #     stock.day_change = current_status_dict['day_change']
    #     stock.day_change_percentage = current_status_dict['day_change_percentage']
    #     stock.save()
    # except ObjectDoesNotExist as e:
    #     CurrentRate.objects.create(**current_status_dict)


def update_historical_rates_bulk_insert(list_of_hist_rates):
    # try:
    #     last_update = HistoricalRate.objects.filter(symbol_id='VTI').get(trading_date=HistoricalRate.objects.latest('trading_date').trading_date).trading_date
    # except ObjectDoesNotExist as e:
    list_of_obj = []
    for date_info in list_of_hist_rates:
        obj = HistoricalRate(**date_info)
        list_of_obj.append(obj)
    HistoricalRate.objects.bulk_create(list_of_obj)

# get historical data using jason
def get_hist_data(request,symbol):
    response = requests.get(request)
    list_of_hist_rates = []
    if response.status_code == 200:
        data = json.loads(response.text)
        i=0
        try:
            last_update = HistoricalRate.objects.filter(symbol_id=symbol)\
                .get(trading_date=HistoricalRate.objects.latest('trading_date').trading_date).trading_date
        except ObjectDoesNotExist as e:
            last_update=datetime.date(2014,12,30)
        for timestamp in data['chart']['result'][0]['timestamp']:
            dict = {}
            result_path = data['chart']['result'][0]
            path = result_path['indicators']['quote'][0]
            trading_date = datetime.datetime.fromtimestamp(timestamp).date()
            if trading_date>last_update:
                dict['trading_date'] =trading_date
                dict['open_price'] = path['open'][i]
                dict['high_price'] = path['high'][i]
                dict['low_price'] = path['low'][i]
                dict['close_price'] = path['close'][i]
                dict['adj_close_price'] = result_path['indicators']['adjclose'][0]['adjclose'][i]
                dict['symbol_id'] = result_path['meta']['symbol']
                list_of_hist_rates.append(dict)
            i += 1
    else:
        print("error")
    return list_of_hist_rates


def update_historical_dividends(request):
    response = requests.get(request)
    if response.status_code==200:
        data = json.loads(response.text)
        symbol=data['chart']['result'][0]['meta']['symbol']
        try:
            dividend_list= list((data['chart']['result'][0]['events']['dividends'].keys()))
            for date in dividend_list:
                date_to_update = datetime.datetime.fromtimestamp(int(date)).date()
                obj = HistoricalRate.objects.filter(trading_date=date_to_update).get(symbol_id=symbol)
                obj.dividend_amount = data['chart']['result'][0]['events']['dividends'][date]['amount']
                obj.save()
        except KeyError as e:
            pass


def modified_request(symbol):
    try:
        last_update = HistoricalRate.objects.filter(symbol_id=symbol)\
            .get(trading_date=HistoricalRate.objects.latest('trading_date').trading_date).trading_date + datetime.timedelta(days=1)
        last_update = str(int(datetime.datetime(year=last_update.year, month=last_update.month, day=last_update.day)
                              .timestamp()))
    except ObjectDoesNotExist as e:
        last_update='1420063200'
    now_timestamp = str(int(datetime.datetime.today().timestamp()))
    modified_request ="https://query2.finance.yahoo.com/v8/finance/chart/"+symbol+"?formatted=true&crumb=0ZXdu.gWVfg&lang=en-US&region=US&interval=1d&period1="+last_update+"&period2="+now_timestamp+"&events=div%7Csplit&corsDomain=finance.yahoo.com"
    return modified_request


def update_hist_rates_for_stocks(): #happens every day
    # request ="https://query2.finance.yahoo.com/v8/finance/chart/VTI?formatted=true&crumb=0ZXdu.gWVfg&lang=en-US&region=US&interval=1d&period1=992552400&period2=1575583200&events=div%7Csplit&corsDomain=finance.yahoo.com"
    for stock in Stock.objects.all():
        symbol=stock.symbol
        request = modified_request(symbol)
        update_historical_rates_bulk_insert(get_hist_data(request,symbol))
        update_historical_dividends(request)


    # update_current_rate(get_current_rates_webscraping("https://finance.yahoo.com/quote/VT?p=VT&.tsrc=fin-srch"))

update_hist_rates_for_stocks()


def func_to_time():
    get_current_rates_webscraping("https://finance.yahoo.com/quote/VT?p=VT&.tsrc=fin-srch")


# print(timeit.timeit(func_to_time, number=5))
print("end")

'''--------------------------------------------------------------------------------------------------------------'''


# gets first page of histoical rates using web scraping
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
            dict['date'] = datetime.datetime.strptime(values[0], '%b %d, %Y')
            dict['open_price'] = values[1]
            dict['high_price'] = values[2]
            dict['low_price'] = values[3]
            dict['close_price'] = values[4]
            dict['adj_close_price'] = values[5]
            dict['symbol_id'] = symbol_id
            list_of_hist_rates.append(dict)
        elif values[1] == 'Dividend':
            dict['symbol_id'] = symbol_id
            dict['date'] = datetime.datetime.strptime(values[0], '%b %d, %Y')
            dict['dividend'] = values[1]
            dict['dividend_amount'] = row.find('strong').get_text()
    return list_of_hist_rates

# gets current_rates using web scraping- takes more time
def get_current_rates_webscraping(request):
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