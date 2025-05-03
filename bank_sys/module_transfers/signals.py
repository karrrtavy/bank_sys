from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from module_account.models import Account
from module_card.models import Card
from .models import TransactionHistory

@receiver(post_save, sender=Account)
def log_account_creation(sender, instance, created, **kwargs):
    if created:
        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type='account_create',
            description=f'Создан счет №{instance.number}',
            source_account=instance
        )

@receiver(post_delete, sender=Account)
def log_account_deletion(sender, instance, **kwargs):
    TransactionHistory.objects.create(
        user=instance.user,
        transaction_type='account_delete',
        description=f'Удален счет №{instance.number}'
    )

@receiver(post_save, sender=Card)
def log_card_creation(sender, instance, created, **kwargs):
    if created:
        TransactionHistory.objects.create(
            user=instance.account.user,
            transaction_type='card_create',
            description=f'Создана карта ****{instance.number[-4:]}',
            source_account=instance.account,
            card=instance
        )

@receiver(post_delete, sender=Card)
def log_card_deletion(sender, instance, **kwargs):
    TransactionHistory.objects.create(
        user=instance.account.user,
        transaction_type='card_delete',
        description=f'Удалена карта ****{instance.number[-4:]}',
        source_account=instance.account
    )
