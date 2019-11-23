from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from finance.models import OptimalPortfolios


class Users(User):
    '''
        all users .is updated when a new user subscribes and in the settings page of every user
    '''
    username = models.CharField(max_length=150, primary_key=True)
    optimal_portfolio = models.ForeignKey(OptimalPortfolios, on_delete=models.SET_NULL, null=True)
    daily_commission_percentage = models.FloatField(default=0)
    daily_commission_const = models.FloatField(default=0)
    ending_date_for_commission_contract = models.DateField(auto_now=False, auto_now_add=False)