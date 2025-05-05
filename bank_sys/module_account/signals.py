from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from module_auth.models import User
from .models import Account
from module_card.models import Card
from module_transfers.models import TransactionHistory

@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """
    @brief Обработчик сигнала post_save для модели User.
    @details Автоматически создаёт основной аккаунт и основную карту при создании нового пользователя.
    
    @param sender Класс модели, который вызвал сигнал (User).
    @param instance Экземпляр модели User, который был сохранён.
    @param created Логический флаг, указывающий, был ли создан новый объект (True при создании).
    @param kwargs Дополнительные параметры сигнала.
    
    @return None
    """
    if created:
        account = Account.objects.create(
            user=instance,
            is_primary=True,
            balance=50000
        )
        
        Card.objects.create(
            account=account,
            is_primary=True
        )