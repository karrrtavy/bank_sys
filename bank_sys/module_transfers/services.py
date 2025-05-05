from module_card.models import Card
from module_account.signals import TransactionHistory
from .models import TransactionHistory

@staticmethod
def transfer_by_card(sender_card, receiver_card_number, amount):
    """
    @brief Выполняет перевод средств с одной карты на другую.
    @details Проверяет наличие достаточного баланса на счёте отправителя,
             списывает сумму с аккаунта отправителя и зачисляет на аккаунт получателя,
             создаёт записи в истории транзакций для обеих сторон.
    
    @param sender_card Объект карты отправителя (Card).
    @param receiver_card_number Номер карты получателя (str).
    @param amount Сумма перевода (Decimal или float).
    
    @var receiver_card Объект карты получателя, блокируемый для обновления (select_for_update).
    
    @throws ValueError Если недостаточно средств на счёте отправителя.
    @return None
    """
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
        transaction_type='transfer_out',
        amount=amount,
        description=f'Перевод на карту ****{receiver_card.number[-4:]}',
        source_account=sender_card.account,
        destination_account=receiver_card.account,
        card=sender_card
    )
    
    TransactionHistory.objects.create(
        user=receiver_card.account.user,
        transaction_type='transfer_in',
        amount=amount,
        description=f'Получение от карты ****{sender_card.number[-4:]}',
        source_account=receiver_card.account,
        destination_account=sender_card.account,
        card=receiver_card
    )
