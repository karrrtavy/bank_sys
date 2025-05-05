from django.db import models
from module_auth.models import User
import random
import string

# Create your models here.

class Account(models.Model):
    """
    @brief Модель банковского аккаунта пользователя.
    @details Хранит информацию об аккаунте, включая номер, баланс, статус основного аккаунта и дату создания.
    
    @var user Внешний ключ на пользователя (User), которому принадлежит аккаунт.
    @var number Уникальный номер аккаунта, генерируется автоматически, не редактируется вручную.
    @var is_primary Логический флаг, указывающий, является ли аккаунт основным для пользователя.
    @var balance Текущий баланс аккаунта с точностью до двух знаков после запятой.
    @var created_at Дата и время создания аккаунта, устанавливается автоматически.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True, editable=False)
    is_primary = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        @brief Переопределённый метод сохранения модели.
        @details При сохранении автоматически генерирует уникальный номер аккаунта,
                 если он отсутствует, и устанавливает флаг is_primary, если у пользователя
                 ещё нет основного аккаунта.
        
        @param args Позиционные аргументы, передаваемые в базовый метод save.
        @param kwargs Именованные аргументы, передаваемые в базовый метод save.
        @return None
        """
        if not self.number:
            self.number = self.generate_account_number()

        if not self.pk:
            if not Account.objects.filter(user=self.user, is_primary=True).exists():
                self.is_primary = True

        super().save(*args, **kwargs)

    @classmethod
    def generate_account_number(cls):
        """
        @brief Генерирует уникальный 20-значный номер аккаунта.
        @details Использует случайный выбор цифр, проверяет уникальность в базе данных.
        
        @return str Уникальный номер аккаунта длиной 20 символов.
        """
        while True:
            number = ''.join(random.choices(string.digits, k=20))
            if not cls.objects.filter(number=number).exists():
                return number
            
    def __str__(self):
        """
        @brief Строковое представление объекта Account.
        @return str Строка с номером аккаунта и текущим балансом.
        """
        return f"№{self.number} (Баланс: {self.balance} ₽)"
    
    @property
    def cards_total_balance(self):
        """
        @brief Вычисляет суммарный баланс всех связанных карт аккаунта.
        @details Использует связь обратную к модели Card через card_set.
        
        @return Decimal Общий баланс всех карт, связанных с данным аккаунтом.
        """
        return sum(card.balance for card in self.card_set.all())
