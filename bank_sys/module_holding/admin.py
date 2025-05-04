from django.contrib import admin
from .models import Holding

# Register your models here.
@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('user', 'account', 'balance', 'created_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('user__phone', 'account__number')
    readonly_fields = ('last_interest_date',)