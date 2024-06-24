
from contrib.utils import generate_64bit_uuid

def update_user_checkouts_count(instance) -> None:
    """ Set a Checkout Count to the User model `checkout_count` field"""
    customer = instance.customer # User Model Object
    customer.checkouts_count += 1
    customer.save()

def set_unique_id() -> int:
    uuid = generate_64bit_uuid()
    return uuid