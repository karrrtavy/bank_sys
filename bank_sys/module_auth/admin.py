from django.contrib import admin
from .models import User
from module_account.models import Account
from module_card.models import Card

# Register your models here.

class AccountInline(admin.TabularInline):
    """
    @brief Встраиваемый класс для отображения связанных аккаунтов в админке пользователя.
    @details Позволяет редактировать и просматривать связанные объекты Account прямо на странице User.
    
    @var model Модель, которая отображается инлайн (Account).
    @var extra Количество пустых форм для добавления новых объектов (0 - не показывать).
    @var show_change_link Показывать ссылку на изменение связанного объекта (True).
    """
    model = Account
    extra = 0
    show_change_link = True

class CardInline(admin.TabularInline):
    """
    @brief Встраиваемый класс для отображения связанных карт в админке.
    @details Позволяет редактировать и просматривать связанные объекты Card на странице другого объекта.
    
    @var model Модель, которая отображается инлайн (Card).
    @var extra Количество пустых форм для добавления новых объектов (0 - не показывать).
    @var show_change_link Показывать ссылку на изменение связанного объекта (True).
    """
    model = Card
    extra = 0
    show_change_link = True

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    @brief Класс настройки административного интерфейса для модели User.
    @details Определяет отображаемые поля, фильтры, поиск, порядок сортировки и встроенные модели.
    
    @var list_display Кортеж полей модели User, отображаемых в списке.
    @var search_fields Кортеж полей, по которым осуществляется поиск.
    @var list_filter Кортеж полей для фильтрации списка.
    @var fieldsets Кортеж, определяющий группы полей и их расположение в форме редактирования.
    @var ordering Кортеж полей для сортировки списка пользователей.
    @var inlines Список встроенных классов для отображения связанных моделей (например, AccountInline).
    """
    list_display = ('phone', 'name', 'surname', 'income', 'is_staff')
    search_fields = ('phone', 'name', 'surname')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'patronymic', 'income')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    ordering = ('phone',)
    inlines = [AccountInline]