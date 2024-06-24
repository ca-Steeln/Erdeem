
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from accounts.utils import create_member_account
from wallets.utils import create_member_wallet

user_model = get_user_model()

@receiver(post_save, sender=user_model)
def post_user(sender, instance, created, **kwargs):
    if created:
        create_member_account(member=instance)
        create_member_wallet(member=instance)
