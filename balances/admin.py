
from django.contrib import admin

from .models import Balance

# Register your models here.

class BalanceAdmin(admin.ModelAdmin):
    model = Balance
    readonly_fields = ['wallet', 'currency', 'amount', 'created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(amount=0)

admin.site.register(Balance, BalanceAdmin)
