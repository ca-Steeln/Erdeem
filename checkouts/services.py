
from requests.exceptions import HTTPError
from requests import Response
from typing import Dict

from django.conf import settings

from chargily_pay import ChargilyClient
from chargily_pay.entity import Checkout, CheckoutItem, Customer, Product, Price


# ! Make all these functions into a Chargily Api class

chargily_gateway = ChargilyClient(
        key=settings.CHARGILY_KEY,
        secret=settings.CHARGILY_SECRET,
        url=settings.CHARGILY_URL,
    )

def get_balance():
    return chargily_gateway.get_balance()

def fetch_chargily_object(data:list[dict], **kwargs) -> dict:
    """ Find the dict object in data list """
    # Check if all kwargs match
    for item in data:
        if all(item.get(key) == value for key, value in kwargs.items()):
            return item


def get_chargily_customer_id(customer) -> str:

    try:
        customer_id = getattr(settings, 'CHARGILY_TESTER_CUSTOMER_ID') or customer.chargily_entity_id
    except AttributeError:
        return customer.chargily_entity_id
    return customer_id

def get_chargily_product_id(product) -> str:
    try:
        product_id = getattr(settings, 'CHARGILY_TESTER_PRODUCT_ID') or product.chargily_entity_id
    except AttributeError:
        return product.chargily_entity_id
    return product_id


def create_empty_checkout(checkout):
    """ Create checkout within Chargily Checkout datatype class """

    item = checkout.items
    entity:dict = checkout.to_chargily_entity()
    entity["amount"] = int(item.amount)
    entity["currency"] = checkout.payment_currency

    checkout_entity = Checkout(**entity)
    response = chargily_gateway.create_checkout(checkout=checkout_entity)
    checkout.chargily_entity_id = response["id"]
    checkout.checkout_url = response["checkout_url"]
    checkout.save()
    return checkout

def create_item_checkout(checkout):
    """ Create `Chargily` Checkout within Product """
    customer = checkout.customer
    customer_id = get_chargily_customer_id(customer)
    item = checkout.items
    item_amount = int(item.amount)
    price = get_or_create_chargily_price(
        item, item_amount, checkout.payment_currency
    )

    entity: dict = checkout.to_chargily_entity()
    entity["customer_id"] = customer_id
    entity["items"] = [CheckoutItem(price["id"], checkout.quantity)]

    checkout_entity = Checkout(**entity)
    response = chargily_gateway.create_checkout(checkout=checkout_entity)
    checkout.chargily_entity_id = response["id"]
    checkout.checkout_url = response["checkout_url"]
    checkout.save()

    return checkout


def create_customer(entity: dict) -> Customer:
    """ Create `Chargily` Customer using `settings.AUTH_USER_MODEL` instance """
    customer = Customer(**entity)
    return chargily_gateway.create_customer(customer=customer)

def get_or_create_customer(entity: dict) -> Customer:
    try:
        customers = chargily_gateway.list_customers()
        customer = fetch_chargily_object(customers['data'], **entity)
        if not customer:
            raise HTTPError
        return customer

    except HTTPError:
        return create_customer(entity)


def create_product(entity: dict) -> Product:
    """ Product attr takes The Product Model instance """
    product = Product(**entity)
    return chargily_gateway.create_product(product=product)

def get_or_create_product(entity: dict) -> Product:
    try:
        products = chargily_gateway.list_products()
        product_item = fetch_chargily_object(
            products['data'], name=entity['name']
        )
        if not product_item: raise HTTPError
        return product_item

    except HTTPError:
        return create_product(entity)


# Create Chargily Price for the Product
def create_chargily_price(product: Product, amount: int, payment_currency: str):
    product_id = get_chargily_product_id(product)
    return chargily_gateway.create_price(
        Price(
            amount = amount,
            currency = payment_currency,
            product_id = product_id,
        )
    )

# Get or Create Chargily Price for the Product
def get_or_create_chargily_price(
        product: Product, amount: int, payment_currency: str
    ) -> Price:

    product_id = get_chargily_product_id(product)
    try:
        prices = chargily_gateway.retrieve_product_prices(product_id)
        price_item = fetch_chargily_object(
            prices['data'],
            amount=amount,
            currency=payment_currency
        )
        if price_item: return price_item
        raise HTTPError

    except HTTPError:
        return create_chargily_price(
            product, amount, payment_currency
        )


# Create Chargily a Checkout Items for the checkout
def make_chargily_checkout_items(items, payment_currency: str) -> list[CheckoutItem]:
    """ `items` attr takes Order Model instances within fields: `product`, `quantity` """

    checkout_items = []
    for item in items:
        price = get_or_create_chargily_price(
            item.product,
            item.product.amount,
            payment_currency
        )
        checkout_items.append(CheckoutItem(price=price['id'], quantity=item.quantity))
    return checkout_items








