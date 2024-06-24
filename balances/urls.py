
from django.urls import path

from .views import BalancesView, BalanceView

app_name = 'balances'

urlpatterns = [
    path('', BalancesView.as_view(), name='balances'),
    path('<str:currency_code>', BalanceView.as_view(), name='balance'),
]
