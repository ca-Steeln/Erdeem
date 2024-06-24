
from django.core.exceptions import ValidationError

def alpha_validator(value):
    if not any(char.isalpha() for char in value):
        raise ValidationError('Username must contain at least one letter.')