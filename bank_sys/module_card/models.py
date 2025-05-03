from django.db import models
from module_account.models import Account
import random
import string

# Create your models here.
class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, unique=True, editable=False)
    is_primary = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number} ('Баланс: {self.balance:.2f} ₽')"

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_card_number()

        if not self.pk:
            if not Card.objects.filter(account=self.account, is_primary=True).exists():
                self.is_primary = True

        super().save(*args, **kwargs)

    @classmethod
    def generate_card_number(cls):
        while True:
            number = '4' + ''.join(random.choices(string.digits, k=15))
            if not cls.objects.filter(number=number).exists():
                return number