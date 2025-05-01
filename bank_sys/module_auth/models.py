from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator

# Create your models here.
class User (models.Model):
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
    patronymic = models.CharField(max_length=50, blank=True)

    def clean(self):
        name_regex = RegexValidator(
            regex=r'^[а-яА-ЯёЁ\s]+$',
            message="ФИО должно содержать только русские буквы"
        )
        for field in [self.last_name, self.first_name, self.patronymic]:
            if field:
                name_regex(field)