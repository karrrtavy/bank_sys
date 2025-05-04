from django import forms
from .models import Holding
from module_account.models import Account
from django.core.validators import MinValueValidator

class HoldingCreateForm(forms.ModelForm):
    class Meta:
        model = Holding
        fields = ['account']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)

class HoldingDepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        label="Сумма пополнения"
    )

class HoldingWithdrawForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        label="Сумма изъятия"
    )