
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from contrib.utils import check_uniqueness

from .models import Transaction
from .utils import set_unique_id, set_unique_slug

@receiver(pre_save, sender=Transaction)
def pre_transaction(sender, instance, **kwargs):

    if not instance.id or check_uniqueness(sender, id=instance.id):
        instance.id = set_unique_id()

    if not instance.slug or check_uniqueness(sender, slug=instance.slug):
        instance.slug = set_unique_slug()