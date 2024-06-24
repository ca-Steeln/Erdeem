
from django.urls import path
from .views import WalletView, DepositView, WithdrawalView, SendToUserView

app_name = 'wallets'

urlpatterns = [
    path('', WalletView.as_view(), name='wallet'),

    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdrawal/', WithdrawalView.as_view(), name='withdrawal'),
    path('send/', SendToUserView.as_view(), name='send'),
]
