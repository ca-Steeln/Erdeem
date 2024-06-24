
from decimal import Decimal

from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from checkouts.services import get_or_create_product

from .utils import generate_currency_min_amount

# Create your models here.
class Currency(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=12, unique=True)
    symbol = models.CharField(max_length=5, null=True, blank=True)

    min_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(max_length=1000, null=True, blank=True, default=None)

    chargily_id = models.CharField(max_length=50, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def directory_path(instance, filename): return f"currencies/{instance.code}/{filename}"
    def default_directory_path(): return "default/currencies/currency.jpg"
    image = models.ImageField(upload_to=directory_path, default=default_directory_path, blank=True)

    exchange_rate_to_usd = models.DecimalField(verbose_name=_('Exchange Rate To USD'), max_digits=20, decimal_places=4, null=True)
    exchange_rate_to_dzd = models.DecimalField(verbose_name=_('Exchange Rate To DZD'), max_digits=20, decimal_places=4, null=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.code

    def to_entity(self) -> dict:
        return {
            'name': self.code,
            'description': self.description or None,
        }

@receiver(pre_save, sender=Currency)
def pre_currency(sender, instance, *args, **kwargs):
    if not instance.chargily_id:
        # Create Chargily product using that instance
        entity: dict = instance.to_entity()
        product = get_or_create_product(entity)
        instance.chargily_id = product['id']

    # ! set exchange_rate_to_usd & exchange_rate_to_dzd

    instance.min_amount = generate_currency_min_amount(
        exchange_rate_to_usd=instance.exchange_rate_to_usd
        )