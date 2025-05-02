from module_card.models import Card
from module_account.signals import TransactionHistory

@staticmethod
def transfer_by_card(sender_card, receiver_card_number, amount):
    receiver_card = Card.objects.select_for_update().get(
        number=receiver_card_number
    )
    
    if sender_card.account.balance < amount:
        raise ValueError("Недостаточно средств")
    
    sender_card.account.balance -= amount
    sender_card.account.save()
    
    receiver_card.account.balance += amount
    receiver_card.account.save()
    
    TransactionHistory.objects.create(
        user=sender_card.account.user,
        transaction_type='transfer',
        amount=amount,
        description=f'Перевод на карту ****{receiver_card.number[-4:]}',
        source_account=sender_card.account,
        destination_account=receiver_card.account,
        card=sender_card
    )
    
    TransactionHistory.objects.create(
        user=receiver_card.account.user,
        transaction_type='transfer',
        amount=amount,
        description=f'Получение от карты ****{sender_card.number[-4:]}',
        source_account=receiver_card.account,
        destination_account=sender_card.account,
        card=receiver_card
    )
