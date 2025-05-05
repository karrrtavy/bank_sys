from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Holding
from module_transfers.models import TransactionHistory

@receiver(post_save, sender=Holding)
def log_holding_creation(sender, instance, created, **kwargs):
    """
    @brief Обработчик сигнала post_save для модели Holding.
    @details При создании нового объекта Holding создаёт запись в истории транзакций.
    
    @param sender Класс модели, вызвавший сигнал (Holding).
    @param instance Экземпляр модели Holding, который был сохранён.
    @param created Логический флаг, указывающий, был ли создан новый объект (True при создании).
    @param kwargs Дополнительные параметры сигнала.
    
    @return None
    """
    if created:
        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type='holding_create',
            description='Создание нового вклада',
            source_account=instance.account
        )

@receiver(post_delete, sender=Holding)
def log_holding_deletion(sender, instance, **kwargs):
    """
    @brief Обработчик сигнала post_delete для модели Holding.
    @details При удалении объекта Holding создаёт запись в истории транзакций.
    
    @param sender Класс модели, вызвавший сигнал (Holding).
    @param instance Экземпляр модели Holding, который был удалён.
    @param kwargs Дополнительные параметры сигнала.
    
    @return None
    """
    TransactionHistory.objects.create(
        user=instance.user,
        transaction_type='holding_delete',
        description=f'Удаление вклада №{instance.id}'
    )
