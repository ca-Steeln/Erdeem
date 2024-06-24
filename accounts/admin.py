
from django.contrib import admin
from .models import Account

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    model = Account
    readonly_fields = ['member', 'birthday', 'locale', 'theme', 'country', 'transactions_count', 'chargily_id', 'slug']

admin.site.register(Account, AccountAdmin)