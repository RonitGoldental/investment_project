from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.decorators import api_view
from finance.models import InvestmentUser, PortfolioManagement, Stock
from finance.permissions import IsOwnerOrReadOnly
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
        serializer.save(user=self.request.user)


class PortfolioManagementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PortfolioManagement.objects.all()
    serializer_class = PortfolioManagementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'portfolio management': reverse('portfolio-management-log', request=request, format=format),
        'stocks': reverse('stock-list', request=request, format=format)
    })
