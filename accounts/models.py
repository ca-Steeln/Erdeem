
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify

from core.validators import alpha_validator


# Create your models here.

class Account(models.Model):

    class Locale(models.TextChoices):
        EN = 'en', _('English')
        AR = 'ar', _('Arabic')
        FR = 'fr', _('French')

    class Theme(models.TextChoices):
        light = 'light', _('Light')
        dark = 'dark', _('Dark')

    class COUNTRIES(models.TextChoices):
        DZ = 'DZ', _('Algeria')


    member = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account')
    name = models.CharField(max_length=50, blank=True, validators=[alpha_validator])
    phone = PhoneNumberField(max_length=13)

    def directory_path(instance, filename): return f"accounts/avatars/{instance.member.id}/{slugify(filename)}"
    def default_directory_path(): return "default/accounts/avatar.jpg"
    avatar = models.ImageField(upload_to=directory_path, default=default_directory_path, blank=True)
    description = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    locale = models.CharField(max_length=255, choices=Locale.choices, default=Locale.EN)
    theme = models.CharField(max_length=255, choices=Theme.choices, default=Theme.light)
    country = models.CharField(max_length=255, choices=COUNTRIES.choices, default=COUNTRIES.DZ)

    transactions_count = models.PositiveIntegerField(blank=True, default=0)
    chargily_id = models.CharField(max_length=255, unique=True, blank=True)

    slug = models.SlugField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.slug})

    def to_entity(self) -> dict:
        return {
            'name': self.member.username,
            'email': self.member.email,
            'phone': self.phone or None,
            'address': {
                'country': self.country or None,
                # 'state': self.state,
                # 'address': self.address
            }
        }
