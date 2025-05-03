from django import forms
from module_account.models import Account
from module_card.models import Card

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(
        queryset=Account.objects.none(),
        label="Счет списания"
    )
    from_card = forms.ModelChoiceField(
        queryset=Card.objects.none(),
        label="Карта списания",
        required=False
    )
    to_account_number = forms.CharField(
        label="Номер счета получателя",
        required=False,
        help_text="Для перевода другому пользователю"
    )
    to_card_number = forms.CharField(
        label="Номер карты получателя",
        required=False,
        help_text="Для перевода на карту"
    )
    amount = forms.DecimalField(
        label="Сумма",
        min_value=0.01,
        decimal_places=2
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['from_account'].queryset = Account.objects.filter(user=user)
        self.fields['from_card'].queryset = Card.objects.filter(account__user=user)
