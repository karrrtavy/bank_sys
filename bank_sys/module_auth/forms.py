from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class RegistrationForm(forms.ModelForm):
    """
    @brief Форма регистрации нового пользователя.
    @details Расширяет стандартную ModelForm, добавляя поля для пароля и подтверждения пароля,
             а также валидацию совпадения паролей.
    
    @var password Поле для ввода пароля с виджетом PasswordInput.
    @var repeat_password Поле для повторного ввода пароля для подтверждения.
    """

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
        """
        @brief Мета-класс для настройки модели и полей формы.
        
        @var model Модель User, на основе которой строится форма.
        @var fields Список полей модели, включённых в форму.
        @var labels Словарь с пользовательскими метками для полей.
        @var help_texts Словарь с подсказками для полей.
        """
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

    def clean(self):
        """
        @brief Выполняет дополнительную валидацию формы.
        @details Проверяет, что поля password и repeat_password совпадают.
        
        @var cleaned_data Словарь с очищенными данными формы.
        @var password Значение поля password из очищенных данных.
        @var repeat_password Значение поля repeat_password из очищенных данных.
        
        @return dict Очищенные данные формы.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        
        if password and repeat_password and password != repeat_password:
            self.add_error('repeat_password', 'Пароли не совпадают')
        
        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    """
    @brief Кастомная форма аутентификации пользователя.
    @details Позволяет вводить в поле username либо логин, либо телефон.
    
    @var username Поле для ввода логина или телефона с подсказкой.
    @var password Поле для ввода пароля с виджетом PasswordInput.
    """
    username = forms.CharField(
        label="Логин или телефон",
        help_text="Введите телефон (+7...) или имя пользователя"
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput
    )
