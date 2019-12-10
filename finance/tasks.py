import json
import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
import datetime
import timeit
import grequests

# django setup
import os
import django

from finance.task_utils import modified_request_hist_rates, update_historical_rates_bulk_insert, update_hist_rate_for_symbol

os.environ['DJANGO_SETTINGS_MODULE'] = 'investment_portfolio.settings'
django.setup()

from finance.models import CurrentRate, HistoricalRate, Stock




def update_hist_rates_for_stocks(): #happens every day
    # request ="https://query2.finance.yahoo.com/v8/finance/chart/VTI?formatted=true&crumb=0ZXdu.gWVfg&lang=en-US&region=US&interval=1d&period1=992552400&period2=1575583200&events=div%7Csplit&corsDomain=finance.yahoo.com"
    for stock in Stock.objects.all():
        symbol=stock.symbol
        request = modified_request_hist_rates(symbol)
        update_hist_rate_for_symbol(request,symbol)


print(timeit.timeit(update_hist_rates_for_stocks, number=1))

# update_hist_rates_for_stocks()

print("end task")