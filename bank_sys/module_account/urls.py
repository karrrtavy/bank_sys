from django.contrib import admin
from django.urls import path
from .views import AccountDetailView, AccountCreateView, CardCreateView, AccountDeleteView, CardDeleteView, CardMakePrimaryView, AccountMakePrimaryView

urlpatterns = [
    path('account/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('account/create/', AccountCreateView.as_view(), name='account_create'),
    path('account/<int:account_id>/card/create/', CardCreateView.as_view(), name='card_create'),
    path('account/<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete'),
    path('card/<int:card_id>/delete/', CardDeleteView.as_view(), name='card_delete'),
    path('card/<int:card_id>/make_primary/', CardMakePrimaryView.as_view(), name='card_make_primary'),
    path('account/<int:pk>/make_primary/', AccountMakePrimaryView.as_view(), name='account_make_primary'),
]