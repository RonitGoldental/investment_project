from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.decorators import api_view
from finance.models import InvestmentUser, PortfolioManagement, Stock
from finance.permissions import IsOwnerOrReadOnly
from finance.serializers import InvestmentUserSerializer, PortfolioManagementSerializer, StockSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class InvestmentUserSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = InvestmentUser.objects.all()
    serializer_class = InvestmentUserSerializer

class StockSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class PortfolioManagementSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = PortfolioManagement.objects.all()
    serializer_class = PortfolioManagementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



