from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_backends
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm, CustomLoginForm

# Create your views here.
class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'module_auth/sign_up.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        from django.contrib.auth import get_backends
        backend = get_backends()[0]
        login(self.request, user, backend=backend.__module__ + '.' + backend.__class__.__name__)
        return redirect(self.get_success_url())
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

class Login(LoginView):
    form_class = CustomLoginForm
    template_name = 'module_auth/sign_in.html'
    redirect_authenticated_user = True