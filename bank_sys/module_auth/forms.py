from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['name', 'surname', 'patronymic', 
                  'phone', 'income', 'password', 
                  'repeat_password']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин или телефон")