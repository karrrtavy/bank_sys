from django.urls import path
from .views import holdings_view, credit_withdraw_view

urlpatterns = [
    path('holdings/', holdings_view, name='holdings'),
    path('credit/withdraw/', credit_withdraw_view, name='credit_withdraw'),
]