
from .models import Account

def create_member_account(member) -> Account:
    return Account.objects.create(member=member)