
from django.contrib import admin

from .models import Transaction

# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    readonly_fields = [
        'id', 'merchant', 'recipient', 'balance', 'currency', 'amount',
        'transaction_type', 'payment_method', 'withdrawal_destination',
        'description', 'created_at',
    ]

admin.site.register(Transaction, TransactionAdmin)
