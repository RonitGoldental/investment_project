from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from finance import views
from django.conf.urls import include

urlpatterns = [
    path('investmentuser/', views.InvestmentUserList.as_view(), name="user-list"),
    path('investmentuser/<int:pk>/', views.InvestmentUsertDetail.as_view()),
    path('portfoliomanagement/', views.PortfolioManagementList.as_view(), name="portfolio-management-log"),
    path('portfoliomanagement/<int:pk>/', views.PortfolioManagementDetail.as_view()),
    path('stock/', views.StockList.as_view(), name="stock-list"),
    path('stock/<int:pk>/', views.StockDetail.as_view()),
    path('', views.api_root),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)