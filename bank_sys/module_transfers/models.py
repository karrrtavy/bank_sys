from django.db import models
from module_auth.models import User
from module_account.models import Account
from module_card.models import Card

# Create your models here.
class TransactionHistory(models.Model):
    TRANSACTION_TYPES = (
        ('transfer', 'Перевод'),
        ('account_create', 'Создание счета'),
        ('card_create', 'Создание карты'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=255)
    source_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='source_transactions')
    destination_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='destination_transactions')
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
