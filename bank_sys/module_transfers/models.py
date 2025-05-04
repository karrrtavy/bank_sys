from django.db import models
from module_auth.models import User
from module_account.models import Account
from module_card.models import Card

# Create your models here.
class TransactionHistory(models.Model):
    TRANSACTION_TYPES = (
        ('account_create', 'Создание счета'),
        ('account_delete', 'Удаление счета'),
        ('card_create', 'Создание карты'),
        ('card_delete', 'Удаление карты'),
        ('transfer_in', 'Зачисление'),
        ('transfer_out', 'Списание'),
        ('holding_deposit', 'Пополнение вклада'),
        ('holding_withdraw', 'Изъятие с вклада'),
        ('holding_interest', 'Начисление процентов'),
        ('holding_close', 'Закрытие вклада'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    source_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='history_source')
    target_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='history_target')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.timestamp}"