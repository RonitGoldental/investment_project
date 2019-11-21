from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Stocks(models.Model):
    """
    a table that contains all the stocks and compatible risk. is updated once and than manually
    """
    symbol = models.CharField(max_length = 10, primary_key = True)
    stack_name = models.CharField(max_length= 70)
    #sector = models.CharField(max_length= 70)
    type = models.CharField(max_length= 70) #todo give choises
    risk_factor = models.CharField(max_length= 70) #I decide according to type #todo sort according to type

class HistoricalRates(models.Model):
    """
    all the rates of the stocks and dividend. Is updated one per day
    """
    symbol = models.ForeignKey(Stocks)
    date = models.DateField(auto_now=False, auto_now_add=False)
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    adj_close_price = models.FloatField()
    dividend_paid = models.FloatField()


class Current_rates(models.Model):
    """
    all the rates of the stocks now. Is updated every min
    """
    symbol = models.ForeignKey(Stocks)
    current_price = models.FloatField()
    day_change = models.FloatField()
    day_change_percentage = models.FloatField()
    # volume = models.IntegerField()

class OptimalPortfolios(models.Model):
    '''
        updated once by admin but every user can make his own and add
    '''
    portfolio_name= models.CharField(max_length = 50, primary_key = True)
    #low risk
    pre_bonds_gov_usa =  models.FloatField(validators=[MinValueValidator(0,message="Should be between 0 to 1)"),MaxValueValidator(1, message="Should be between 0 to 1")])
    pre_bonds_gov_global = models.FloatField(validators=[MinValueValidator(0,message="Should be between 0 to 1)"),MaxValueValidator(1, message="Should be between 0 to 1")])
    pre_cash = models.FloatField(validators=[MinValueValidator(0,message="Should be between 0 to 1)"),MaxValueValidator(1, message="Should be between 0 to 1")])
    #low medium risk
    pre_bonds_industrial_usa =  models.FloatField(validators=[MinValueValidator(0,message="Should be between 0 to 1)"),MaxValueValidator(1, message="Should be between 0 to 1)")])
    pre_bonds_industrial_global = models.FloatField()
    #medium risk
    pre_usa_stocks = models.FloatField()
    pre_global_stocks = models.FloatField()
    pre_israel_stocks = models.FloatField()
    pre_gold = models.FloatField()
    pre_goods = models.FloatField()
    pre_individual_bonds = models.FloatField()
    #high_risk
    pre_emerging_markets_stocks = models.FloatField()
    pre_real_estate = models.FloatField()
    pre_individual_stocks =  models.FloatField()
    pre_bonds_gov_emerging_markets = models.FloatField()
    pre_bonds_industrial_emerging_markets = models.FloatField()

class Users(models.Model):
    '''
        all users .is updated when a new user subscribes and in the settings page of every user
    '''
    username = models.CharField(max_length = 10, primary_key = True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    email=models.EmailField()
    optimal_portfolio = models.ForeignKey(OptimalPortfolios, on_delete=models.SET_NULL())
    daily_commission_percentage = models.FloatField()
    monthly_commission_percentage = models.FloatField()
    quarterly_commissions_percentage = models.FloatField()
    annual_commission_percentage = models.FloatField()
    daily_commission_const = models.FloatField()
    monthly_commission_const = models.FloatField()
    quarterly_commissions_const = models.FloatField()
    annual_commission_const = models.FloatField()
    ending_date_for_commission_contract = models.DateField(auto_now=False, auto_now_add=False)

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
    user = symbol = models.ForeignKey(Users)
    symbol = models.CharField(max_length=10)
    amount_bought = models.IntegerField() #todo - if only part of the amount is sold
    is_active = models.BooleanField(default=0)
    purchase_date = models.DateField(auto_now=False, auto_now_add=False)
    purchase_commission = models.FloatField(default=0)
    purchase_price = models.FloatField()
    sell_commission = models.FloatField(default=0)
    sale_date = models.DateField(auto_now=False, auto_now_add=False)
    # action = models.CharField(max_length=10)

class QuarterlyCommissions(models.Model):
    '''
        all user anual commisions.is updated every quarter/month when comission is paid
    '''
    user = models.CharField(max_length=10, primary_key = True)
    commission_date = models.DateField(auto_now=False, auto_now_add=False)
    commission_paid = models.FloatField()
 #todo - think if per stock or not







