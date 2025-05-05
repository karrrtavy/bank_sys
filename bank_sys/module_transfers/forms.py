from django import forms
from module_account.models import Account
from module_card.models import Card

TRANSFER_FROM_CHOICES = [
    ('account', 'Списать со счета'),
    ('card', 'Списать с карты'),
]

TRANSFER_TO_CHOICES = [
    ('account', 'Перевести на счет'),
    ('card', 'Перевести на карту'),
]

class TransferForm(forms.Form):
    """
    @brief Форма для осуществления переводов между счетами и картами.
    @details Позволяет выбрать источник списания (счет или карта), указать счет или карту отправителя,
             выбрать тип получателя (счет или карта), ввести номер получателя и сумму перевода.
    
    @var transfer_from Поле выбора источника списания: счет или карта.
    @var sender_account Поле выбора счета отправителя, доступно только для текущего пользователя.
    @var sender_card Поле выбора карты отправителя, доступно только для текущего пользователя.
    @var transfer_to Поле выбора типа получателя: счет или карта.
    @var receiver_number Текстовое поле для ввода номера счета или карты получателя.
    @var amount Десятичное поле для ввода суммы перевода, минимальное значение 0.01.
    """

    transfer_from = forms.ChoiceField(choices=TRANSFER_FROM_CHOICES, label="Откуда списать")
    sender_account = forms.ModelChoiceField(queryset=Account.objects.none(), label="Счет отправителя", required=False)
    sender_card = forms.ModelChoiceField(queryset=Card.objects.none(), label="Карта отправителя", required=False)
    transfer_to = forms.ChoiceField(choices=TRANSFER_TO_CHOICES, label="Куда перевести")
    receiver_number = forms.CharField(label="Номер счета/карты получателя")
    amount = forms.DecimalField(label="Сумма", min_value=0.01)

    def __init__(self, *args, **kwargs):
        """
        @brief Конструктор формы.
        @details Инициализирует queryset для полей sender_account и sender_card, фильтруя по текущему пользователю.
        
        @param args Позиционные аргументы.
        @param kwargs Именованные аргументы, должен содержать ключ 'user' с объектом пользователя.
        """
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['sender_account'].queryset = Account.objects.filter(user=user)
        self.fields['sender_card'].queryset = Card.objects.filter(account__user=user)
