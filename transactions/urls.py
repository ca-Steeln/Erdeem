
from django.urls import path
from .views import TransactionsView, TransactionView


app_name = 'transactions'

urlpatterns = [

    path('', TransactionsView.as_view(), name='transactions'),
    path('<slug:slug>/', TransactionView.as_view(), name='transaction'),
]
