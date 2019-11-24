from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from finance.models import InvestmentUser, OptimalPortfolio, Stock,\
    CurrentRate, HistoricalRate, QuarterlyCommission, PortfolioManagement
# Register your models here.

admin.site.register(InvestmentUser, UserAdmin)
admin.site.register(OptimalPortfolio)
admin.site.register(Stock)
admin.site.register(CurrentRate)
admin.site.register(HistoricalRate)
admin.site.register(QuarterlyCommission)
admin.site.register(PortfolioManagement)

