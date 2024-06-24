
from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.core.validators import MinValueValidator

from currencies.models import Currency
from members.utils import update_user_checkouts_count

from .utils import create_slug


class Checkout(models.Model):

    # Choices
    class PAYMENT_STATUS(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        FAILED = "FAILED", _("Failed")
        CANCELED = "CANCELED", _("Canceled")
        EXPIRED = "EXPIRED", _("Expired")

    class PAYMENT_METHODS(models.TextChoices):
        EDAHABIA = "edahabia", _("Edahabia")
        CIB = "cib", "CIB"

    class PAYMENT_CURRENCIES(models.TextChoices):
        DZD = 'dzd', _('DZD')

    # Validators
    def min_quantity(limit_value=5):
        return MinValueValidator(
            limit_value= limit_value,
            message = _(f'Quantity must be at least {limit_value}')
        )

    # Fields
    chargily_entity_id = models.CharField(max_length=255, unique=True, blank=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    amount = models.PositiveIntegerField(null=True, blank=True)
    payment_currency = models.CharField(_("Currency"), max_length=3, choices=PAYMENT_CURRENCIES.choices)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS.choices, default=PAYMENT_METHODS.EDAHABIA)
    note = models.TextField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING)
    checkout_url = models.URLField()

    items = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False, blank=False)
    quantity =  models.PositiveIntegerField(default=5, validators=[min_quantity()])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    slug = models.SlugField(unique=True, blank=True)

    def on_paid(self):
        self.status = self.PaymentStatus.PAID
        self.save()
        # after success payment process

    def on_failure(self):
        self.status = self.PaymentStatus.FAILED
        self.save()

    def on_cancel(self):
        self.status = self.PaymentStatus.CANCELED
        self.save()

    def on_expire(self):
        self.status = self.PaymentStatus.EXPIRED
        self.save()

    def to_chargily_entity(self) -> dict:
        return {
            'amount': self.amount,
            'currency': None,
            'success_url': 'https://chargily.com/',
            'items': None,
            'payment_method': self.payment_method,
            'customer_id': self.customer.chargily_entity_id or None,
            'failure_url': None,
            'webhook_endpoint': None,
            'description' : self.note or None,
            'locale': self.customer.locale,
            'pass_fees_to_customer': False,
        }

    def __str__(self) -> str:
        return f'checkout id: {self.id}'

    def get_absolute_url(self):
        return reverse("checkouts:checkout", kwargs={"slug": self.slug})


@receiver(pre_save, sender=Checkout)
def pre_checkpoint(sender, instance, *args, **kwargs):
    if not instance.slug: create_slug(instance)

@receiver(post_save, sender=Checkout)
def post_checkpoint(sender, instance, created, *args, **kwargs):
    if created: update_user_checkouts_count(instance)
