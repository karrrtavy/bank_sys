from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm, CustomLoginForm

# Create your views here.
class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'module_auth/sign_up.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.user)
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

class Login(LoginView):
    form_class = CustomLoginForm
    template_name = 'module_auth/sign_in.html'
    redirect_authenticated_user = True