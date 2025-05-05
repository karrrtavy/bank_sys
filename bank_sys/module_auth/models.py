from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator

# Create your models here.

class User(AbstractUser):
    """
    @brief Кастомная модель пользователя, расширяющая AbstractUser.
    @details Добавляет поле телефона с валидацией, доход и ФИО с проверкой на русские буквы.
    
    @var phone_regex Валидатор для проверки формата номера телефона.
    @var phone Телефон пользователя, уникальное поле, формат +7XXXXXXXXXX.
    @var income Ежемесячный доход пользователя, неотрицательное десятичное число.
    @var surname Фамилия пользователя, необязательное поле.
    @var name Имя пользователя, необязательное поле.
    @var patronymic Отчество пользователя, необязательное поле.
    """

    phone_regex = RegexValidator(
        regex=r'^\+7\d{10}$',
        message="Номер должен быть в формате: '+7 123 456 78 90'"
    )
    phone = models.CharField(
        max_length=12,
        validators=[phone_regex],
        unique=True    
    )
    income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        blank=True,
        null=True
    )
    surname = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    patronymic = models.CharField(max_length=50, blank=True)

    def clean(self):
        """
        @brief Выполняет валидацию полей ФИО.
        @details Проверяет, что фамилия, имя и отчество содержат только русские буквы и пробелы.
        
        @var name_regex Регулярное выражение для проверки русских букв.
        @var fields_to_validate Список значений полей для проверки.
        
        @return None
        @throws ValidationError Если одно из полей содержит недопустимые символы.
        """
        name_regex = RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s]+$',
            message="ФИО должно содержать только русские буквы"
        )
        fields_to_validate = [
            self.surname, 
            self.name, 
            self.patronymic
        ]
        for field in fields_to_validate:
            if field:
                name_regex(field)

    def get_full_name(self):
        """
        @brief Возвращает полное имя пользователя.
        @details Формирует строку из фамилии, имени и отчества, разделённых пробелами,
                 убирая лишние пробелы в начале и конце.
        
        @return str Полное имя пользователя.
        """
        return f"{self.surname} {self.name} {self.patronymic}".strip()
    
    def save(self, *args, **kwargs):
        """
        @brief Переопределённый метод сохранения модели.
        @details Если поле username не задано, устанавливает его равным номеру телефона.
        
        @param args Позиционные аргументы для базового метода save.
        @param kwargs Именованные аргументы для базового метода save.
        @return None
        """
        if not self.username:
            self.username = self.phone
        super().save(*args, **kwargs)
