
from django.utils.text import slugify

from string import ascii_lowercase, ascii_uppercase
from random import shuffle, randint
from uuid import uuid4

def create_slug(instance, save=False) -> None:
    """
    Create and set the new slug to `instance.slug`.
    """
    model = instance.__class__
    customer = instance.customer # User Model Object

    slug_template: str = f'{customer.username}-checkout-{customer.checkouts_count}'
    slug = slugify(slug_template)

    slug_exists = model.objects.filter(slug=slug).exists()
    if slug_exists:
        # uuid in case slug exists
        slug = slugify(create_uuid4())

    instance.slug = slug


def create_uuid4(min_char:int = 4, max_char:int = 6) -> str:
    s1 = list(ascii_lowercase)
    s2 = list(ascii_uppercase)
    s4 = list(slugify(uuid4()))

    characters_number = randint(min_char, max_char)
    shuffle(s1)
    shuffle(s2)

    slug = []
    for i in range(round(characters_number * (60/100))):
        slug.append(s1[i])
        slug.append(s2[i])

    for i in range(round(characters_number * (40/100))):
        slug.append(s4[i])

    shuffle(slug)
    return "".join(slug)