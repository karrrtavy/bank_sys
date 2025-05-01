from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator

# Create your models here.
class User (AbstractUser):
    phone_regex = RegexValidator (
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
        validators=[MinValueValidator(0)]
    )
    surname = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    patronymic = models.CharField(max_length=50, blank=True)

    def clean(self):
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