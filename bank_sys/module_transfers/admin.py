from django.contrib import admin
from .models import TransactionHistory

# Register your models here.
@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'description', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('user__phone', 'description')