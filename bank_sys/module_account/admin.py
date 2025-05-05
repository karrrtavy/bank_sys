from django.contrib import admin
from .models import Account
from module_card.models import Card

# Register your models here.

class CardInline(admin.TabularInline):
    """
    @brief Вспомогательный класс для отображения связанных карт в админке аккаунта.
    @details Используется для отображения и редактирования объектов Card, связанных с Account, на одной странице.
    @var model Модель, которая будет отображаться инлайн (Card).
    @var extra Количество пустых форм для добавления новых объектов (0 - не отображать пустые формы).
    @var show_change_link Показывать ли ссылку на изменение объекта (True).
    """
    model = Card
    extra = 0
    show_change_link = True

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """
    @brief Класс для настройки отображения модели Account в административной панели Django.
    @details Позволяет настраивать список отображаемых полей, фильтры, поиск и инлайны связанных моделей.
    
    @var list_display Кортеж с именами полей Account, которые будут отображаться в списке объектов.
    @var search_fields Кортеж с именами полей, по которым будет осуществляться поиск.
    @var list_filter Кортеж с именами полей, по которым можно фильтровать список.
    @var inlines Список инлайн-классов для отображения связанных моделей (CardInline).
    """
    list_display = ('number', 'user', 'balance', 'is_primary', 'created_at')
    search_fields = ('number', 'user__phone')
    list_filter = ('is_primary',)
    inlines = [CardInline]