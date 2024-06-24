
from typing import Any
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class MinCurrencyAmount(MinValueValidator):
    message = _("Currency amount must be at least or equal to %(limit_value)s.")
