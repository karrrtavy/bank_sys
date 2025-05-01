from django.contrib import admin
from django.urls import path
from .views import Registration, Login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Registration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]