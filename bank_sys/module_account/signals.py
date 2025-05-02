from django.db.models.signals import post_save
from django.dispatch import receiver
from module_auth.models import User
from .models import Account
from module_card.models import Card
from module_transfers.models import TransactionHistory

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        account = Account.objects.create(
            user=instance,
            is_primary=True,
            balance=50000
        )

        TransactionHistory.objects.create(
            user=instance,
            transaction_type='account_create',
            description=f'Создан счет №{account.number}',
            source_account=account
        )
        
        Card.objects.create(
            account=account,
            is_primary=True
        )

        TransactionHistory.objects.create(
            user=instance,
            transaction_type='card_create',
            description=f'Создана карта ****{Card.number[-4:]}',
            source_account=account,
            card=Card
        )