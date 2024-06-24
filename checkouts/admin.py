

from django.contrib import admin

from .models import Checkout

# Register your models here.

class CheckoutAdmin(admin.ModelAdmin):
    model = Checkout
    readonly_fields = ['customer', 'status', 'amount', 'items', 'quantity', 'payment_currency', 'payment_method', 'chargily_entity_id', 'created_at', 'updated_at',  'note', 'slug']

admin.site.register(Checkout, CheckoutAdmin)