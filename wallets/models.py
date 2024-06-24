
from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Sum, DecimalField
from django.db.models.functions import Coalesce

from currencies.utils import calc_currency_amount_value

# Create your models here.


class Wallet(models.Model):
    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    total_balance_as_usd = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, editable=False)
    total_balance_as_dzd = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.member}'s Wallet"


    def update_total_balances(self):
        """ Updates total balances for client's dashboard as USD & DZD in Total """
        self.total_balance_as_usd = "%.2f" % self.balances.annotate(
            amount_usd=F('amount') * F('currency__exchange_rate_to_usd')
        ).aggregate(total_usd=Coalesce(Sum('amount_usd', output_field=DecimalField(max_digits=20, decimal_places=2)), Decimal('0.00')))['total_usd']

        self.total_balance_as_dzd = "%.2f" % self.balances.annotate(
            amount_dzd=F('amount') * F('currency__exchange_rate_to_dzd')
        ).aggregate(total_dzd=Coalesce(Sum('amount_dzd', output_field=DecimalField(max_digits=20, decimal_places=2)), Decimal('0.00')))['total_dzd']

        self.save()

    def get_amounted_balances(self):
        """ Get only balances with an amount in them """
        return self.balances.exclude(amount=0)

    def get_recent_balances(self, length:int=3):
        """ Get recent active balances objects that has been updated in range of attr `length` """
        balances = self.get_amounted_balances()
        return list(balances.order_by('-updated_at').only('id', 'amount', 'updated_at')[:length])