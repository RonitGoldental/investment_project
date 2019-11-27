from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from finance import views
from django.conf.urls import include
from finance.views import PortfolioManagementSet, InvestmentUserSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from finance import views
# InvestmentUserList = InvestmentUserSet.as_view({
#     'get': 'list'
# })
# InvestmentUserDetail = InvestmentUserSet.as_view({
#     'get': 'retrieve'
# })
# PortfolioManagementList = PortfolioManagementSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# PortfolioManagementDetail = PortfolioManagementSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# StockList = InvestmentUserSet.as_view({
#     'get': 'list'
# })
# StockDetail = InvestmentUserSet.as_view({
#     'get': 'retrieve'
# })


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'PortfolioManagement', views.PortfolioManagementSet)
router.register(r'InvestmentUser', views.InvestmentUserSet)
router.register(r'Stock', views.StockSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
#
# urlpatterns = [
#     path('investmentuser/', InvestmentUserList,name="user-list"),
#     path('investmentuser/<int:pk>/',InvestmentUserDetail),
#     path('portfoliomanagement/',PortfolioManagementList, name="portfolio-management-log"),
#     path('portfoliomanagement/<int:pk>/', PortfolioManagementDetail),
#     path('stock/', StockList, name="stock-list"),
#     path('stock/<int:pk>/', StockDetail),
#     path('', views.api_root),
# ]
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls')),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)