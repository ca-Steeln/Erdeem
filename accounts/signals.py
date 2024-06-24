
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.conf import settings

from checkouts.services import get_or_create_customer

from .models import Account

model = Account

@receiver(pre_save, sender=model)
def pre_user(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.member.username)

    if not instance.name:
        instance.name = instance.member.username

    try:
        if not instance.chargily_id:
            entity: dict = instance.to_entity()
            customer = get_or_create_customer(entity)
            instance.chargily_id = customer['id']
    except:
        if settings.DEBUG:
            raise

