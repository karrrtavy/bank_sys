from django.contrib import admin
from .models import TransactionHistory

# Register your models here.

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    """
    @brief Класс настройки административного интерфейса для модели TransactionHistory.
    @details Определяет отображаемые поля, фильтры и поля для поиска в админке.
    
    @var list_display Кортеж полей модели TransactionHistory, отображаемых в списке объектов.
    @var list_filter Кортеж полей для фильтрации списка объектов.
    @var search_fields Кортеж полей, по которым осуществляется поиск.
    """
    list_display = ('user', 'transaction_type', 'description', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('user__phone', 'description')
