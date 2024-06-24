
import shortuuid
from uuid import uuid4

from django.db.models import Model
from django.utils import timezone

from .models import get_model

def check_uniqueness(klass: Model|str, **kwargs) -> bool:
    """
    Checks object existence. True means does exists, False otherwise.
    """
    model_manager = get_model(klass).objects
    return model_manager.filter(**kwargs).exists()

def generate_64bit_uuid() -> int:
    # Generate a 128-bit UUID and use the lower 64 bits
    uuid = uuid4().int & (1 << 63) - 1
    return uuid

def generate_unique_slug(length: int = 12) -> str:
    """
    Generate unique slug. max length 22
    example: "9JtPrwXnFoGtRbV8yXsh3a"
    """
    return shortuuid.uuid()[:length]