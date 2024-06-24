
from .base import *
from config.env import env

# Django
DEBUG = env.bool('DJANGO_DEBUG', default=True)

# Mail Config
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Chargily Api config
CHARGILY_URL = env('CHARGILY_TEST_URL')
CHARGILY_KEY = env('CHARGILY_TEST_KEY')
CHARGILY_SECRET = env('CHARGILY_TEST_SECRET')
CHARGILY_TESTER_CUSTOMER_ID = env('CHARGILY_TESTER_CUSTOMER_ID')
CHARGILY_TESTER_PRODUCT_ID = env('CHARGILY_TESTER_PRODUCT_ID')