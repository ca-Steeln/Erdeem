
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from core.validators import alpha_validator
from .utils import set_unique_id


class Member(AbstractUser):
    id = models.BigIntegerField(primary_key=True, default=set_unique_id, unique=True, db_index=True, editable=False)
    username = models.CharField(max_length=34, unique=True, validators=[alpha_validator], db_index=True)


