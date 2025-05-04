from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Holding
from module_transfers.models import TransactionHistory

@receiver(post_save, sender=Holding)
def log_holding_creation(sender, instance, created, **kwargs):
    if created:
        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type='holding_create',
            description='Создание нового вклада',
            source_account=instance.account
        )

@receiver(post_delete, sender=Holding)
def log_holding_deletion(sender, instance, **kwargs):
    TransactionHistory.objects.create(
        user=instance.user,
        transaction_type='holding_delete',
        description=f'Удаление вклада №{instance.id}'
    )