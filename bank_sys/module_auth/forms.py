from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        help_text="Введите надежный пароль"
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Повторите пароль",
        help_text="Повторите пароль для подтверждения"
    )
    
    class Meta:
        model = User
        fields = ['name', 'surname', 'patronymic', 
                'phone', 'income', 'password', 
                'repeat_password']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'patronymic': 'Отчество',
            'phone': 'Телефон',
            'income': 'Доход',
        }
        help_texts = {
            'phone': 'Формат: +71234567890',
            'income': 'Укажите ваш ежемесячный доход',
            'name': 'Только русские буквы',
            'surname': 'Только русские буквы',
            'patronymic': 'Только русские буквы',
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин или телефон",
        help_text="Введите телефон (+7...) или имя пользователя"
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )