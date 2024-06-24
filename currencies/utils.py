
from django.conf import settings

def get_usd_equivalent(exchange_rate_to_usd:float, amount:float = 1.00):
    """
    Calculate the equivalent amount in USD for a given amount of another currency.
    Returns:
        float: The equivalent amount in USD.
    """
    return amount / exchange_rate_to_usd

def generate_currency_min_amount(exchange_rate_to_usd:float):
    """ Calculates & generate currency minimum amount according to `settings.MIN_TRANSACTION_AMOUNT_IN_USD` """
    min_amount_in_usd = getattr(settings, 'MIN_TRANSACTION_AMOUNT_IN_USD')
    min_amount = get_usd_equivalent(exchange_rate_to_usd, min_amount_in_usd)
    return min_amount

def calc_currency_amount_value(exchange_rate, amount:int):
    """ Calculate the value of the currency amount according to exchange_rate """
    return exchange_rate * amount


