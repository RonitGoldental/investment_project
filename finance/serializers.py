from finance.models import InvestmentUser, OptimalPortfolio, Stock, \
    CurrentRate, HistoricalRate, QuarterlyCommission, PortfolioManagement
from rest_framework import serializers


class InvestmentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentUser
        fields = '__all__'

class OptimalPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimalPortfolio
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class CurrentRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentRate
        fields = '__all__'


class HistoricalRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalRate
        user = serializers.ReadOnlyField(source='user.username')
        fields = '__all__'

'''
class QuarterlyCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterlyCommission
        fields = '__all__'
'''

class PortfolioManagementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = PortfolioManagement
        fields = '__all__'
