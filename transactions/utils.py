

from random import randint

from contrib.utils import generate_64bit_uuid, generate_unique_slug

# store value here, to avoid saving function's path to the instance field.
def set_unique_id() -> int:
    uuid = generate_64bit_uuid()
    return uuid

def set_unique_slug() -> str:
    length = randint(8, 10)
    uuid = generate_unique_slug(length)
    return uuid
