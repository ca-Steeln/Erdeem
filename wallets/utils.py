
from .models import Wallet

def create_member_wallet(member) -> Wallet:
    return Wallet.objects.create(member=member)

def get_or_create_member_wallet(member) -> Wallet:
    return Wallet.objects.get_or_create(member=member)