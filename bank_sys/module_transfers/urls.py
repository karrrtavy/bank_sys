from django.contrib import admin
from django.urls import path
from views import TransferView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transfer/', TransferView.as_view(), name='transfer'),
]