
from django.contrib import admin

from .models import Wallet

# Register your models here.

class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    readonly_fields = ['member', 'total_balance_as_usd', 'total_balance_as_dzd', 'created_at', 'updated_at']

admin.site.register(Wallet, WalletAdmin)