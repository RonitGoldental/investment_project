from datetime import datetime

from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# COMMON VALIDATORS:
from django.utils import timezone

zero_to_one = [MinValueValidator(0, message="Should be between 0 to 1)"),
               MaxValueValidator(1, message="Should be between 0 to 1")]


# Create your models here.


class OptimalPortfolio(models.Model):
    '''
        updated once by admin but every user can make his own and add
    '''
    portfolio_name = models.CharField(max_length=50, primary_key=True)
    # low risk
    pre_bonds_gov_usa = models.FloatField(validators=zero_to_one)
    pre_bonds_gov_global = models.FloatField(validators=zero_to_one)
    pre_cash = models.FloatField(validators=zero_to_one)
    # low medium risk
    pre_bonds_industrial_usa = models.FloatField(validators=zero_to_one)
    pre_bonds_industrial_global = models.FloatField(validators=zero_to_one)
    # medium risk
    pre_usa_stocks = models.FloatField(validators=zero_to_one)
    pre_global_stocks = models.FloatField(validators=zero_to_one)
    pre_israel_stocks = models.FloatField(validators=zero_to_one)
    pre_gold = models.FloatField(validators=zero_to_one)
    pre_goods = models.FloatField(validators=zero_to_one)
    pre_individual_bonds = models.FloatField(validators=zero_to_one)
    # high_risk
    pre_emerging_markets_stocks = models.FloatField(validators=zero_to_one)
    pre_real_estate = models.FloatField(validators=zero_to_one)
    pre_individual_stocks = models.FloatField(validators=zero_to_one)
    pre_bonds_gov_emerging_markets = models.FloatField(validators=zero_to_one)
    pre_bonds_industrial_emerging_markets = models.FloatField(validators=zero_to_one)
    # todo validation that sum = 1


class InvestmentUser(AbstractUser):
    '''
        all users .is updated when a new user subscribes and in the settings page of every user
    '''
    optimal_portfolio = models.ForeignKey(OptimalPortfolio, on_delete=models.SET_NULL, null=True)
    daily_commission_percentage = models.FloatField(default=0)
    daily_commission_const = models.FloatField(default=0)
    ending_date_for_commission_contract = models.DateField(auto_now=False, auto_now_add=False, null=True)


class Stock(models.Model):
    """
    a table that contains all the stocks and compatible risk. is updated once and than manually
    """
    # sector = models.CharField(max_length= 70)
    symbol = models.CharField(max_length=10, primary_key=True)
    stock_name = models.CharField(max_length=70)
    type = models.CharField(max_length=70)  # todo give choises
    risk_factor = models.CharField(max_length=70)  # I decide according to type #todo sort according to type

    # def __str__(self):
    #     return self.symbol

class HistoricalRate(models.Model):
    """
    all the rates of the stocks and dividend. Is updated one per day
    """
    symbol = models.ForeignKey(Stock, models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    adj_close_price = models.FloatField()
    dividend_amount = models.FloatField(default=0)

    # def __str__(self):
    #     return self.symbol+" "+"self.date"



class CurrentRate(models.Model):
    """
    all the rates of the stocks now. Is updated every min
    """ # todo datetime
    time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now())
    symbol = models.ForeignKey(Stock, models.CASCADE)
    current_price = models.FloatField()
    day_change = models.FloatField()
    day_change_percentage = models.FloatField()
    # volume = models.IntegerField()

    def __str__(self):
        return self.symbol_id


'''
class CurrentPortfolios(models.Model):  #todo is needed?
    symbol = models.CharField(max_length=10)  # todo fK
    user = models.CharField(max_length = 10) # todo fK
    amount =models.IntegerField()
    purchase_date = models.DateField(auto_now=False, auto_now_add=False)
    purchase_price = models.FloatField()
    current_price = models.FloatField()
    #dividend_paid = models.FloatField(default=0)
    #commission_paid = models.FloatField(default=0)
    day_change= models.FloatField()
    day_change_percentage = models.FloatField()
    total_change = current_price/purchase_price*100
'''


class PortfolioManagement(models.Model):
    '''
    all user purchases.is updated by the user on every perchase and every sell
    '''
    user = models.ForeignKey(InvestmentUser, on_delete=models.CASCADE)
    symbol = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount_bought = models.IntegerField()  # todo - if only part of the amount is sold
    is_active = models.BooleanField(default=0)
    purchase_date = models.DateField(auto_now=False, auto_now_add=False)
    purchase_commission = models.FloatField(default=0)
    purchase_price = models.FloatField()
    sell_commission = models.FloatField(default=0)
    sale_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    # action = models.CharField(max_length=10)


class QuarterlyCommission(models.Model):
    '''
        all user anual commisions.is updated every quarter/month when comission is paid
    '''
    user = models.ForeignKey(InvestmentUser, on_delete=models.CASCADE)
    commission_date = models.DateField(auto_now=False, auto_now_add=False)
    commission_paid = models.FloatField()

# todo - think if per stock or not
