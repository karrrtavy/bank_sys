from django.db.models.signals import post_save
from django.dispatch import receiver
from module_auth.models import User
from .models import Account
from module_card.models import Card

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        # Создаем основной счет
        account = Account.objects.create(
            user=instance,
            is_primary=True,
            balance=50000
        )
        
        Card.objects.create(
            account=account,
            is_primary=True
        )