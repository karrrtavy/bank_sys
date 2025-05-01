from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Account
from module_card.models import Card

@receiver(post_save, sender=Account)
def create_initial_card(sender, instance, created, **kwargs):
    if created:
        Card.objects.create(
            account=instance,
            is_primary=True
        )
        instance.balance += 50000
        instance.save()