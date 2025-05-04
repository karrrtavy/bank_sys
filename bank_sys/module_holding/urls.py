from django.urls import path
from .views import holdings_view

urlpatterns = [
    path('holdings/', holdings_view, name='holdings'),
]