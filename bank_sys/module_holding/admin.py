from django.contrib import admin
from .models import Holding

# Register your models here.

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    """
    @brief Класс настройки административного интерфейса для модели Holding.
    @details Определяет отображаемые поля, фильтры, поиск и поля только для чтения в админке.
    
    @var list_display Кортеж полей модели Holding, отображаемых в списке объектов.
    @var list_filter Кортеж полей для фильтрации списка объектов.
    @var search_fields Кортеж полей, по которым осуществляется поиск.
    @var readonly_fields Кортеж полей, доступных только для чтения в форме редактирования.
    """
    list_display = ('user', 'account', 'balance', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__phone', 'account__number')
    readonly_fields = ('last_interest_date',)
