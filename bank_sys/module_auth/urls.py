from django.contrib import admin
from django.urls import path
from .views import Registration, Login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Registration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
]