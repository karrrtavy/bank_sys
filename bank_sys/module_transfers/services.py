from django.db import transaction
from module_card.models import Card

class TransferService:
    @staticmethod
    @transaction.atomic
    def transfer_by_card(sender_card, receiver_card_number, amount):
        receiver_card = Card.objects.select_for_update().get(
            number=receiver_card_number
        )
        
        if sender_card.account.balance < amount:
            raise ValueError("Недостаточно средств")
            
        sender_card.account.balance -= amount
        receiver_card.account.balance += amount
        
        sender_card.account.save()
        receiver_card.account.save()
        
        Transfer.objects.create(
            sender=sender_card.account.user,
            receiver=receiver_card.account.user,
            amount=amount,
            from_card=sender_card,
            to_card=receiver_card
        )