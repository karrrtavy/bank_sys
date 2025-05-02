from django.contrib import admin
from django.urls import path
from .views import AccountDetailView, AccountCreateView, CardCreateView

urlpatterns = [
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('account/create/', AccountCreateView.as_view(), name='account_create'),
    path('account/<int:account_id>/card/create/', CardCreateView.as_view(), name='card_create'),
]