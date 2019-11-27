from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from finance import views
from django.conf.urls import include
from finance.views import PortfolioManagementSet, InvestmentUserSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'portfoliomanagement', views.PortfolioManagementSet)
router.register(r'investmentuser', views.InvestmentUserSet)
router.register(r'stock', views.StockSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]