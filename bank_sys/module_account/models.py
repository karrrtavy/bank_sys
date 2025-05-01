from django.db import models
from module_auth.models import User
from random import random
import string

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True, editable=False)
    is_primary = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.generate_account_number()
        super().save(*args, **kwargs)

    @classmethod
    def generate_account_number(cls):
        while True:
            number = ''.join(random.choices(string.digits, k=20))
            if not cls.objects.filter(number=number).exists():
                return number