
from .base import *
from config.env import env

# Django
DEBUG = env.bool('DJANGO_DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# COOKIES & SESSIONS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Chargily Api config
CHARGILY_URL = env('CHARGILY_URL')
CHARGILY_KEY = env('CHARGILY_KEY')
CHARGILY_SECRET = env('CHARGILY_SECRET')

