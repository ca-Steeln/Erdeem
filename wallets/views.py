
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.conf import settings
from django.db import transaction as db_transaction
from django.core.exceptions import ValidationError
from django.http import Http404
from django.db.models import Model
from django.contrib.auth import get_user_model

from contrib.auth import USER_MODEL
from contrib.auth.decorators import authenticated_only, under_construction
from balances.models import Balance
from wallets.models import Wallet
from transactions.models import Transaction

from .forms import DepositForm, WithdrawalForm, SendToUserForm
from .models import Wallet


# Create your views here.

@method_decorator(authenticated_only, name='dispatch')
class WalletView(DetailView):
    template_name = 'apps/wallets/wallet.html'
    model = Wallet
    context_object_name = 'object'

    def get_object(self) -> Model:
        member = self.request.user
        return get_object_or_404(self.model, member=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        member = self.request.user
        wallet = self.get_object()
        wallet.update_total_balances()
        transactions = Transaction.objects.get_member_transactions(member)

        context["balances_qs"] = wallet.get_recent_balances()
        context["transactions_qs"] = transactions.last_time_transactions(length=10, hours=24)
        return context



@method_decorator(authenticated_only, name='dispatch')
class DepositView(FormView):
    template_name = 'apps/wallets/deposit.html'
    model = Transaction
    form_class = DepositForm
    success_url = reverse_lazy('wallets:wallet')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        member = self.request.user
        context = super().get_context_data(**kwargs)
        context["amounted_balances_qs"] = member.wallet.get_amounted_balances()
        return context

    def form_valid(self, form):
        return self.payment_valid(form)

    def payment_valid(self, form):
        try:
            with db_transaction.atomic():
                self.transaction_valid(form_data=form.cleaned_data)
                super().form_valid(form)
                success(self.request, _('Deposit Transaction Complete Successfully!'))
                return redirect(self.success_url)

        except USER_MODEL.DoesNotExist:
            # ! log the issue, this might be issued when settings.ERDEEM_DEFAULT_MERCHANT_USER_ID DoesNotExist!
            error(self.request, _('Something went wrong. Please try again later!'))
            return super().form_invalid(form)

        except:
            if settings.DEBUG:
                raise
            error(self.request, _('Something went wrong. Deposit Transaction Failed!'))
            return super().form_invalid(form)

    def transaction_valid(self, form_data:dict) -> None:

        merchant = get_user_model().objects.get(id=settings.ERDEEM_MERCHANT_ID)
        recipient = self.get_object()
        currency = form_data['currency']
        amount = form_data['amount']

        with db_transaction.atomic():
            # Fetch or create the balance in the original currency
            balance, created = Balance.objects.get_or_create(wallet=recipient.wallet, currency=currency)

            # Log the deposit transaction
            self.model.objects.create(
                merchant = merchant,
                recipient = recipient,
                balance = balance,
                transaction_type = Transaction.TRANSACTION_TYPES.DEPOSIT,
                **form_data,
            )

            # Update the balance in the original currency
            balance.deposit(amount)


    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

    def transaction_invalid(self):
        pass

@method_decorator(authenticated_only, name='dispatch')
class WithdrawalView(FormView):
    template_name = 'apps/wallets/withdrawal.html'
    model = Transaction
    form_class = WithdrawalForm
    success_url = reverse_lazy('wallets:wallet')

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(WithdrawalView, self).get_form_kwargs()
        kwargs['member'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return self.destination_valid(form)

    def destination_valid(self, form):
        try:
            with db_transaction.atomic():
                self.transaction_valid(form_data=form.cleaned_data)
                super().form_valid(form)
                success(self.request, _('Withdrawal Transaction Complete!'))
                return redirect(self.success_url)

        except ValidationError:
            error(self.request, _('Cannot withdraw an amount greater than your current amount.'))
            return super().form_invalid(form)

        except Balance.DoesNotExist:
            # ! Report Malicious user
            error(self.request, _('The chosen balance is not accessible. Please contact our support team or report the issue!'))
            return super().form_invalid(form)

        except KeyError:
            raise Http404

        except OverflowError:
            # ! log the issue
            error(self.request, 'Unable to process the transaction at this time. Please try again later.')
            return super().form_invalid(form)

        except:
            error(self.request, _('Something went wrong. Withdrawal Transaction Failed!'))
            return super().form_invalid(form)


    def transaction_valid(self, form_data:dict) -> None:

        merchant = get_user_model().objects.get(id=settings.ERDEEM_MERCHANT_ID)
        recipient = self.get_object()
        balance = Balance.objects.get(
            pk=form_data['balance'].pk,
            wallet__member=recipient,
        )
        amount = form_data['amount']

        with db_transaction.atomic():
            # Log the deposit transaction
            transaction = self.model.objects.create(
                merchant = merchant,
                recipient = recipient,
                transaction_type = Transaction.TRANSACTION_TYPES.WITHDRAWAL,
                currency = balance.currency,
                **form_data,
            )

            # Update the balance in the original currency
            balance.withdraw(amount)
        return transaction

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, (field, e))
        return super().form_invalid(form)

    def transaction_invalid(self):
        pass

@method_decorator(under_construction, name='dispatch')
class SendToUserView(FormView):
    template_name = 'apps/wallets/send.html'
    model = Transaction
    form_class = SendToUserForm
    success_url = reverse_lazy('wallets:wallet')