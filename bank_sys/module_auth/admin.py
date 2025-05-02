from django.contrib import admin
from .models import User
from module_account.models import Account
from module_card.models import Card

# Register your models here.
class AccountInline(admin.TabularInline):
    model = Account
    extra = 0
    show_change_link = True

class CardInline(admin.TabularInline):
    model = Card
    extra = 0
    show_change_link = True


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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