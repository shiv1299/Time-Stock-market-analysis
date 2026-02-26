# URLs are defined in stock_dashboard/urls.py
"""
URL configuration for stock_dashboard project.
"""


from django.urls import path
from dashboard import views


urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('company/<str:symbol>/', views.company_dashboard, name='company_dashboard'),
]