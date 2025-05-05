from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from module_account.models import Account
from module_card.models import Card
from .models import TransactionHistory

@receiver(post_save, sender=Account)
def log_account_creation(sender, instance, created, **kwargs):
    """
    @brief Обработчик сигнала post_save для модели Account.
    @details При создании нового аккаунта создаёт запись в истории транзакций о создании счета.
    
    @param sender Класс модели, вызвавший сигнал (Account).
    @param instance Экземпляр модели Account, который был сохранён.
    @param created Логический флаг, указывающий, был ли создан новый объект (True при создании).
    @param kwargs Дополнительные параметры сигнала.
    
    @return None
    """
    if created:
        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type='account_create',
            description=f'Создан счет №{instance.number}',
            source_account=instance
        )

@receiver(post_delete, sender=Account)
def log_account_deletion(sender, instance, **kwargs):
    """
    @brief Обработчик сигнала post_delete для модели Account.
    @details При удалении аккаунта создаёт запись в истории транзакций о удалении счета.
    
    @param sender Класс модели, вызвавший сигнал (Account).
    @param instance Экземпляр модели Account, который был удалён.
    @param kwargs Дополнительные параметры сигнала.
    
    @return None
    """
    TransactionHistory.objects.create(
        user=instance.user,
        transaction_type='account_delete',
        description=f'Удален счет №{instance.number}'
    )

@receiver(post_save, sender=Card)
def log_card_creation(sender, instance, created, **kwargs):
    """
    @brief Обработчик сигнала post_save для модели Card.
    @details При создании новой карты создаёт запись в истории транзакций о создании карты.
    
    @param sender Класс модели, вызвавший сигнал (Card).
    @param instance Экземпляр модели Card, который был сохранён.
    @param created Логический флаг, указывающий, был ли создан новый объект (True при создании).
    @param kwargs Дополнительные параметры сигнала.
    
    @return None
    """
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
    """
    @brief Обработчик сигнала post_delete для модели Card.
    @details При удалении карты создаёт запись в истории транзакций о удалении карты.
    
    @param sender Класс модели, вызвавший сигнал (Card).
    @param instance Экземпляр модели Card, который был удалён.
    @param kwargs Дополнительные параметры сигнала.
    
    @return None
    """
    TransactionHistory.objects.create(
        user=instance.account.user,
        transaction_type='card_delete',
        description=f'Удалена карта ****{instance.number[-4:]}',
        source_account=instance.account
    )
