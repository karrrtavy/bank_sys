from django.contrib import admin
from .models import Account
from module_card.models import Card

# Register your models here.
class CardInline(admin.TabularInline):
    model = Card
    extra = 0
    show_change_link = True

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'balance', 'is_primary', 'created_at')
    search_fields = ('number', 'user__phone')
    list_filter = ('is_primary',)
    inlines = [CardInline]