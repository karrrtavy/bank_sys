from django.db import models
from module_auth.models import User
from module_account.models import Account
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
import random, string

# Create your models here.
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
        
        # рассчет количества минут с последнего начисления
        minutes_passed = (now - self.last_interest_date).total_seconds() / 60
        
        if minutes_passed >= 1:  # Если прошла хотя бы 1 минута
            # +10% каждую минуту
            interest = self.balance * Decimal('0.10') * Decimal(minutes_passed)
            self.balance += interest
            self.last_interest_date = now
            self.save()
            
            # запись в историю операций
            from module_transfers.models import TransactionHistory
            TransactionHistory.objects.create(
                user=self.user,
                transaction_type='holding_interest',
                description=f'Начисление процентов по вкладу ({int(minutes_passed)} мин.)',
                amount=interest
            )
            
            return interest
        return Decimal('0')

    def __str__(self):
        return f"Вклад пользователя {self.user.phone} (Баланс: {self.balance} ₽)"
    
class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, unique=True, editable=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15)  # 15% в минуту
    created_at = models.DateTimeField(auto_now_add=True)
    last_interest_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_card_number()
        super().save(*args, **kwargs)

    @classmethod
    def generate_card_number(cls):
        while True:
            number = '5' + ''.join(random.choices(string.digits, k=15))  # 5 - для кредитных карт
            if not cls.objects.filter(number=number).exists():
                return number

    def calculate_interest(self):
        now = timezone.now()
        if not self.is_active or self.balance >= 0:
            return Decimal('0')
            
        minutes_passed = (now - self.last_interest_date).total_seconds() / 60
        
        if minutes_passed >= 1:
            interest = abs(self.balance) * (self.interest_rate / Decimal('100')) * Decimal(minutes_passed)
            self.balance -= interest
            self.last_interest_date = now
            self.save()
            
            from module_transfers.models import TransactionHistory
            TransactionHistory.objects.create(
                user=self.user,
                transaction_type='credit_interest',
                description=f'Начисление процентов по кредиту ({int(minutes_passed)} мин.)',
                amount=interest,
                card=self
            )
            
            return interest
        return Decimal('0')
    
    def withdraw(self, amount):
        if not self.is_active:
            raise ValueError("Карта не активна")
            
        available = self.credit_limit + self.balance
        
        if amount > available:
            raise ValueError("Превышен кредитный лимит")
            
        self.balance -= amount
        self.save()
        
        # запись в историю операций
        from module_transfers.models import TransactionHistory
        TransactionHistory.objects.create(
            user=self.user,
            transaction_type='credit_withdraw',
            description=f'Снятие с кредитной карты ****{self.number[-4:]}',
            amount=amount,
            card=self
        )
        
        return True

    def __str__(self):
        return f"Кредитная карта {self.number} (Баланс: {self.balance} ₽)"