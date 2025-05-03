from django.contrib import admin
from django.urls import path
from .views import transfer_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transfer/', transfer_view, name='transfer'),
]