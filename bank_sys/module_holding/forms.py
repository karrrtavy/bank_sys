from django import forms
from .models import Holding, CreditCard
from module_account.models import Account
from django.core.validators import MinValueValidator

class HoldingCreateForm(forms.ModelForm):
    """
    @brief Форма создания объекта Holding.
    @details Позволяет выбрать аккаунт пользователя для создания Holding.
    
    Методы:
    @param __init__(*args, **kwargs) Конструктор формы, принимает параметр user для фильтрации аккаунтов.
    """
    class Meta:
        """
        @brief Мета-класс для настройки модели и полей формы.
        
        @var model Модель Holding, на основе которой строится форма.
        @var fields Список полей модели, включённых в форму.
        """
        model = Holding
        fields = ['account']
        
    def __init__(self, *args, **kwargs):
        """
        @brief Конструктор формы.
        @details Извлекает пользователя из kwargs и фильтрует queryset поля account по этому пользователю.
        
        @param args Позиционные аргументы.
        @param kwargs Именованные аргументы, должен содержать ключ 'user' с объектом пользователя.
        """
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)


class HoldingDepositForm(forms.Form):
    """
    @brief Форма для пополнения Holding.
    
    Поля:
    @var amount Десятичное поле для суммы пополнения с минимальным значением 0.01.
    """
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        label="Сумма пополнения"
    )


class HoldingWithdrawForm(forms.Form):
    """
    @brief Форма для изъятия средств из Holding.
    
    Поля:
    @var amount Десятичное поле для суммы изъятия с минимальным значением 0.01.
    """
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        label="Сумма изъятия"
    )


class CreditCardCreateForm(forms.ModelForm):
    """
    @brief Форма создания объекта CreditCard.
    @details Позволяет выбрать аккаунт пользователя для создания кредитной карты.
    
    Методы:
    @param __init__(*args, **kwargs) Конструктор формы, принимает параметр user для фильтрации аккаунтов.
    """
    class Meta:
        """
        @brief Мета-класс для настройки модели и полей формы.
        
        @var model Модель CreditCard, на основе которой строится форма.
        @var fields Список полей модели, включённых в форму.
        """
        model = CreditCard
        fields = ['account']
        
    def __init__(self, *args, **kwargs):
        """
        @brief Конструктор формы.
        @details Извлекает пользователя из kwargs и фильтрует queryset поля account по этому пользователю.
        
        @param args Позиционные аргументы.
        @param kwargs Именованные аргументы, должен содержать ключ 'user' с объектом пользователя.
        """
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)


class CreditCardPayForm(forms.Form):
    """
    @brief Форма для погашения задолженности по кредитной карте.
    
    Поля:
    @var amount Десятичное поле для суммы погашения с минимальным значением 0.01.
    """
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        label="Сумма погашения"
    )


class CreditCardWithdrawForm(forms.Form):
    """
    @brief Форма для снятия средств с кредитной карты.
    
    Поля:
    @var card Поле выбора кредитной карты пользователя, активной.
    @var amount Десятичное поле для суммы снятия с минимальным значением 0.01.
    
    Методы:
    @param __init__(*args, **kwargs) Конструктор формы, принимает параметр user для фильтрации карт.
    """
    card = forms.ModelChoiceField(
        queryset=CreditCard.objects.none(),
        label="Кредитная карта"
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        label="Сумма снятия"
    )
    
    def __init__(self, *args, **kwargs):
        """
        @brief Конструктор формы.
        @details Извлекает пользователя из kwargs и фильтрует queryset поля card по активным кредитным картам пользователя.
        
        @param args Позиционные аргументы.
        @param kwargs Именованные аргументы, должен содержать ключ 'user' с объектом пользователя.
        """
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['card'].queryset = CreditCard.objects.filter(user=user, is_active=True)
