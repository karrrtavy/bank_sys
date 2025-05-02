from django.urls import path
from .views import ProfileView, HistoryView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('history/', HistoryView.as_view(), name='history'),
]