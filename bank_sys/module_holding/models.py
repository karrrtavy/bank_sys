from django.db import models

# Create your models here.
from module_auth.models import User
from module_account.models import Account
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

class Holding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_interest_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def calculate_interest(self):
        now = timezone.now()
        if not self.is_active:
            return
        
        # рассчет количество дней с последнего начисления
        days_passed = (now - self.last_interest_date).days
        
        if days_passed > 0:
            # +10% каждый день
            interest = self.balance * Decimal('0.10') * days_passed
            self.balance += interest
            self.last_interest_date = now
            self.save()
            
            # запись в историю операций
            from module_transfers.models import TransactionHistory
            TransactionHistory.objects.create(
                user=self.user,
                transaction_type='holding_interest',
                description=f'Начисление процентов по вкладу ({days_passed} дн.)',
                amount=interest
            )
            
            return interest
        return Decimal('0')

    def __str__(self):
        return f"Вклад пользователя {self.user.phone} (Баланс: {self.balance} ₽)"