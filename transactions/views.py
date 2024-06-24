
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.conf import settings

from contrib.auth.decorators import authenticated_only

from .models import Transaction


# Create your views here.

@method_decorator(authenticated_only, name='dispatch')
class TransactionsView(ListView):
    template_name = 'apps/transactions/transactions.html'
    model = Transaction
    context_object_name = 'transactions_qs'

    def get_queryset(self):
        member = self.request.user
        return Transaction.objects.get_member_transactions(member)

@method_decorator(authenticated_only, name='dispatch')
class TransactionView(DetailView):
    template_name = 'apps/transactions/transaction.html'
    model = Transaction
    context_object_name = 'object'

    def get_object(self):
        member = self.request.user
        return get_object_or_404(
            klass = Transaction.objects.get_member_transactions(member),
            balance__wallet = member.wallet,
            slug = self.kwargs.get('slug'),
        )
