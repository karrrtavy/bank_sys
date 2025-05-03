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
    transfer_from = forms.ChoiceField(choices=TRANSFER_FROM_CHOICES, label="Откуда списать")
    sender_account = forms.ModelChoiceField(queryset=Account.objects.none(), label="Счет отправителя", required=False)
    sender_card = forms.ModelChoiceField(queryset=Card.objects.none(), label="Карта отправителя", required=False)
    transfer_to = forms.ChoiceField(choices=TRANSFER_TO_CHOICES, label="Куда перевести")
    receiver_number = forms.CharField(label="Номер счета/карты получателя")
    amount = forms.DecimalField(label="Сумма", min_value=0.01)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['sender_account'].queryset = Account.objects.filter(user=user)
        self.fields['sender_card'].queryset = Card.objects.filter(account__user=user)