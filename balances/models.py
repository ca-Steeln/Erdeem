
from decimal import Decimal

from django.db import models, transaction, connection
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.urls import reverse


from wallets.models import Wallet
from currencies.models import Currency

# Create your models here.

class Balance(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='balances', editable=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00), editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        unique_together = ('wallet', 'currency')
        indexes = [
            models.Index(fields=['amount']),
        ]

    def __str__(self):
        return f"{self.currency.code} {self.amount}"

    def get_absolute_url(self):
        return reverse('balances:balance', kwargs={'currency_code': self.currency.code})


    def deposit(self, amount):
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    sql = "UPDATE balances_balance SET amount = amount + %s WHERE id = %s",
                    params = [amount, self.id]
                )
            self.refresh_from_db()
            self.wallet.update_total_balances()

    def withdraw(self, amount):
        self.refresh_from_db()
        if amount <= self.amount:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        sql = "UPDATE balances_balance SET amount = amount - %s WHERE id = %s",
                        params = [amount, self.id]
                    )
                self.refresh_from_db()
                self.wallet.update_total_balances()
                return
        raise ValidationError('The withdrawal amount is greater than the current balance amount.')

