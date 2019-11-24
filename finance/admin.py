from django.contrib import admin
from finance.models import InvestmentUser, OptimalPortfolio, Stock,\
    CurrentRate, HistoricalRate, QuarterlyCommission, PortfolioManagement
# Register your models here.

admin.site.register(InvestmentUser)
admin.site.register(OptimalPortfolio)
admin.site.register(Stock)
admin.site.register(CurrentRate)
admin.site.register(HistoricalRate)
admin.site.register(QuarterlyCommission)
admin.site.register(PortfolioManagement)

