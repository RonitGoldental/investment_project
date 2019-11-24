from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from finance import views
from django.conf.urls import include

urlpatterns = [
    path('investmentuser/', views.InvestmentUserList.as_view()),
    path('investmentuser/<int:pk>/', views.InvestmentUsertDetail.as_view()),
    path('portfoliomanagement/', views.PortfolioManagementList.as_view()),
    path('portfoliomanagement/<int:pk>/', views.PortfolioManagementDetail.as_view()),
    path('stock/', views.StockList.as_view()),
    path('stock/<int:pk>/', views.StockDetail.as_view()),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)