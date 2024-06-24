

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.messages import success, error
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.conf import settings

from contrib.auth.decorators import authenticated_only
from .models import Balance


# Create your views here.

@method_decorator(authenticated_only, name='dispatch')
class BalancesView(ListView):
    template_name = 'apps/balances/balances.html'
    model = Balance
    context_object_name = 'balances_qs'

    def get_queryset(self):
        member = self.request.user
        return member.wallet.get_amounted_balances()

@method_decorator(authenticated_only, name='dispatch')
class BalanceView(DetailView):
    template_name = 'apps/balances/balance.html'
    model = Balance
    context_object_name = 'object'

    def get_object(self):
        member = self.request.user
        amounted_balances = member.wallet.get_amounted_balances()
        return get_object_or_404(
            amounted_balances,
            currency__code=self.kwargs.get('currency_code')
        )