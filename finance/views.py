from django.shortcuts import render
from rest_framework import permissions

from rest_framework import generics

from finance.models import InvestmentUser, PortfolioManagement, Stock
from finance.serializers import InvestmentUserSerializer, PortfolioManagementSerializer, StockSerializer


class InvestmentUserList(generics.ListCreateAPIView):
    queryset = InvestmentUser.objects.all()
    serializer_class = InvestmentUserSerializer


class InvestmentUsertDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvestmentUser.objects.all()
    serializer_class = InvestmentUserSerializer


class StockList(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class PortfolioManagementList(generics.ListCreateAPIView):
    queryset = PortfolioManagement.objects.all()
    serializer_class = PortfolioManagementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PortfolioManagementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PortfolioManagement.objects.all()
    serializer_class = PortfolioManagementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
