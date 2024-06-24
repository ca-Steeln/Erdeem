

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

from balances.models import Balance
from currencies.models import Currency

from .utils import set_unique_id, set_unique_slug


# Create your models here.

class TransactionQuerySet(models.QuerySet):

    def get_member_transactions(self, member):
        return self.filter(Q(merchant=member) | Q(recipient=member))

    def last_time_transactions(self, length:int, **kwargs:timezone.timedelta):
        timestamp = timezone.now() - timezone.timedelta(**kwargs)
        return self.filter(created_at__gte=timestamp).only('id', 'created_at')[:length]

class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

    def get_member_transactions(self, member):
        """ Get all member transactions, whether sender or recipient
            attrs:
                member: settings.AUTH_USER_MODEL object
        """
        return self.get_queryset().get_member_transactions(member)

    def last_time_transactions(self, length:int = 10, **kwargs:timezone.timedelta):
        return self.get_queryset().last_time_transactions(length, kwargs)

class Transaction(models.Model):

    class TRANSACTION_TYPES(models.TextChoices):
        DEPOSIT = 'deposit', _('Deposit')
        WITHDRAWAL = 'withdrawal', _('Withdrawal')
        EXCHANGE = 'exchange', _('Exchange')
        TRANSFER = 'transfer', _('Transfer')
        TRADE = 'trade', _('Trade')

    class TRANSACTION_STATUS(models.TextChoices):
        PENDING = 'pending', _('Pending')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        CANCELLED = 'cancelled', _('Cancelled')
        IN_PROGRESS = 'in_progress', _('In Progress')
        REFUNDED = 'refunded', _('Refunded')
        ON_HOLD = 'on_hold', _('On Hold')
        DISPUTED = 'disputed', _('Disputed')
        EXPIRED = 'expired', _('Expired')

    class PAYMENT_METHODS(models.TextChoices):
        CHARGILY = 'chargily', _('Chargily')
        PAYPAL = 'paypal', _('PayPal')
        GOOGLE_PAY = 'google_pay', _('Google Pay')
        REDOTPAY = 'redotpay', _('Redotpay')

    class WITHDRAWAL_DESTINATION(models.TextChoices):
        EDAHABIA = "edahabia", _("Edahabia")
        CIB = "cib", "CIB"
        PAYPAL = 'paypal', _('PayPal')
        REDOTPAY = 'redotpay', _('Redotpay')

    objects = TransactionManager()

    id = models.BigIntegerField(primary_key=True, default=set_unique_id, unique=True, db_index=True, editable=False)

    merchant = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,  related_name='merchant_transactions')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipient_transactions')

    balance = models.ForeignKey(Balance, on_delete=models.SET_NULL, related_name='transactions', null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS.choices, default=TRANSACTION_STATUS.PENDING)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES.choices)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS.choices, default=PAYMENT_METHODS.CHARGILY, null=True)
    withdrawal_destination = models.CharField(max_length=20, choices=WITHDRAWAL_DESTINATION.choices, default=WITHDRAWAL_DESTINATION.EDAHABIA, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True, blank=True, default=set_unique_slug)

    def __str__(self):
        return f"Transaction {self.id} - {self.amount} {self.currency}"

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['merchant', 'recipient', 'created_at']),
            models.Index(fields=['status', 'transaction_type']),
        ]

    def get_absolute_url(self):
        return reverse("transactions:transaction", kwargs={"slug": self.slug})


    def get_relevant_info(self):
        info = {
            'deposit': {
                _('Payment Through'): self.get_payment_method_display()
            },
            'withdrawal': {
                _('Withdrawal Through'): self.get_withdrawal_destination_display()
            },
        }
        return info[self.transaction_type]


