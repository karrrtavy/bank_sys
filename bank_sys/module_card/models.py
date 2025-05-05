from django.db import models
from module_account.models import Account
import random
import string

# Create your models here.
class Card(models.Model):
    """
    @brief Модель банковской карты, связанной с аккаунтом пользователя.
    @details Хранит информацию о номере карты, балансе, статусе основной карты и дате создания.
    
    @var account Внешний ключ на аккаунт (Account), которому принадлежит карта.
    @var number Уникальный номер карты длиной 16 символов, генерируется автоматически.
    @var is_primary Логический флаг, указывающий, является ли карта основной для аккаунта.
    @var balance Текущий баланс карты с точностью до двух знаков после запятой.
    @var created_at Дата и время создания карты, устанавливается автоматически.
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, unique=True, editable=False)
    is_primary = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        @brief Строковое представление объекта Card.
        @return str Строка с номером карты и текущим балансом.
        """
        return f"{self.number} ('Баланс: {self.balance:.2f} ₽')"

    def save(self, *args, **kwargs):
        """
        @brief Переопределённый метод сохранения модели.
        @details При сохранении автоматически генерирует уникальный номер карты,
                 если он отсутствует, и устанавливает флаг is_primary, если у аккаунта
                 ещё нет основной карты.
        
        @param args Позиционные аргументы для базового метода save.
        @param kwargs Именованные аргументы для базового метода save.
        @return None
        """
        if not self.number:
            self.number = self.generate_card_number()

        if not self.pk:
            if not Card.objects.filter(account=self.account, is_primary=True).exists():
                self.is_primary = True

        super().save(*args, **kwargs)

    @classmethod
    def generate_card_number(cls):
        """
        @brief Генерирует уникальный 16-значный номер карты.
        @details Номер начинается с цифры '4', остальные 15 символов - случайные цифры.
                 Проверяет уникальность номера в базе данных.
        
        @return str Уникальный номер карты длиной 16 символов.
        """
        while True:
            number = '4' + ''.join(random.choices(string.digits, k=15))
            if not cls.objects.filter(number=number).exists():
                return number
