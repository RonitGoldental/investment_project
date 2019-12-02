import requests
from bs4 import BeautifulSoup


def get_symbol(soup):
    name = soup.select("#quote-header-info > div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1")[0].get_text()
    symbol = name.split()[0].strip()
    return symbol


def task1(request):
    response = requests.get(request)
    soup = BeautifulSoup(response.content,"html.parser")
    table_data = soup.select("table")[0] #todo check if there if more than one element
    symbol = get_symbol(soup)
    return (table_data,symbol)


def task2(table_data,symbol):
    list_of_dicts = []
    # dict= {'symbol','date','open_price','high_price','low_price','close_price','adj_close_price','volume'}
    rows = table_data.select("tbody tr")
    for row in rows:
        list_of_spans = row.find_all('span')
        values =[]
        dict={}
        for span in list_of_spans:
            values.append(span.get_text())
        if values[1] != 'Dividend': #todo stock splits and dividend
            dict['date'] = values[0]
            dict['open_price'] = values[1]
            dict['high_price'] = values[2]
            dict['low_price'] = values[3]
            dict['close_price'] = values[4]
            dict['adj_close_price'] = values[5]
            dict['symbol'] = symbol
            list_of_dicts.append(dict)
    return list_of_dicts


table_data,symbol = task1('https://finance.yahoo.com/quote/%5EDJI/history?p=%5EDJI')
list_of_dicts = task2(table_data,symbol)
print(list_of_dicts)
table_data,symbol = task1('https://finance.yahoo.com/quote/JPM/history?p=JPM')
list_of_dicts = task2(table_data,symbol)
print(list_of_dicts)
print("end")
