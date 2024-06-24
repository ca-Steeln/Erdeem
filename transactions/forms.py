
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext as _

from forms.widget import SelectWidget, RadioSelectWidget
from balances.models import Balance
from currencies.models import Currency

from .models import Transaction



class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            self.fields[field].widget.attrs.update(ctx)


class DepositForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['currency', 'amount', 'payment_method', 'description']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            self.fields[field].widget.attrs.update(ctx)

        self.fields['currency'].empty_label = None
        currency_choices = self.fields['currency'].choices
        currency_queryset = self.fields['currency'].queryset
        disabled_choices = [obj.id for obj in currency_queryset.filter(is_active=False).only('id', 'is_active')]

        self.fields['currency'].widget = SelectWidget(choices=currency_choices, disabled_choices=disabled_choices)
        self.fields['payment_method'].required = True
        self.fields['payment_method'].empty_label = None
        self.fields['payment_method'].initial = Transaction.PAYMENT_METHODS.CHARGILY

    def clean(self):

        amount = self.cleaned_data.get('amount')
        currency = self.cleaned_data.get('currency')

        if currency is None:
            raise ValidationError(_('Please select one of the available currencies.'))

        if not isinstance(currency, Currency):
            raise ValidationError(_('An invalid currency was specified, please select a valid currency.'))

        if not currency.is_active:
            return self.add_error(field=None, error={
                    'currency' : ValidationError(_('The specified balance is currently unavailable, please try again later.'))
                }
            )

        if currency.min_amount > amount:
            return self.add_error(field=None, error={
                    'amount' : ValidationError(_(f'The minimum currency amount is {currency.min_amount:.2f} {currency.code}.'))
                }
            )

        return super().clean()

class WithdrawalForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['balance', 'amount', 'withdrawal_destination', 'description']

    def __init__(self, *args, **kwargs) -> None:
        self.member = kwargs.pop('member', None)
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            self.fields[field].widget.attrs.update(ctx)

        self.fields['balance'].empty_label = None
        self.fields['withdrawal_destination'].empty_label = None

        if not self.member:
            raise ValidationError('Couldn\'t find User object in the form kwargs.')

        self.fields['balance'].queryset = Balance.objects.filter(wallet__member = self.member)
        balance_choices = self.fields['balance'].choices
        balance_queryset = self.fields['balance'].queryset
        disabled_choices = [obj.id for obj in balance_queryset.filter(currency__is_active=False).only('id', 'currency')]

        self.fields['balance'].widget = RadioSelectWidget(choices=balance_choices, disabled_choices=disabled_choices)
        self.fields['withdrawal_destination'].required = True
        self.fields['withdrawal_destination'].initial = Transaction.WITHDRAWAL_DESTINATION.EDAHABIA

    def clean(self):

        amount = self.cleaned_data.get('amount')
        balance = self.cleaned_data.get('balance')

        if balance is None:
            raise ValidationError(_('Please select one of the available balances. to make this transaction!'))

        if not isinstance(balance, Balance):
            raise ValidationError(_('An invalid balance was specified, please select a valid balance.'))

        if balance and not balance.wallet == self.member.wallet:
            raise forms.ValidationError(_('The specified balance is not available, please contact our support team.'))

        currency = balance.currency
        if not currency.is_active:
            return self.add_error(field=None, error={
                    'balance' : ValidationError(_('The specified balance is currently unavailable, please try again later.'))
                }
            )

        if currency.min_amount > amount:
            return self.add_error(field=None, error={
                    'amount' : ValidationError(_(f'The minimum currency amount is {currency.min_amount:.2f} {currency.code}.'))
                }
            )

        return super().clean()


class SendToUserForm(forms.ModelForm):
    to = forms.CharField(required=True)

    class Meta:
        model = Transaction
        fields = ['to', 'balance', 'amount', 'description']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            self.fields[field].widget.attrs.update(ctx)

        self.fields['balance'].empty_label = None
        self.fields['to'].label = 'User ID'
