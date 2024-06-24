
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

from .models import Checkout

class SelectWidget(forms.RadioSelect):
    """
    Subclass of Django's select widget that allows disabling options.
    """
    def __init__(self, disabled_choices=None, *args, **kwargs):
        super(SelectWidget, self).__init__(*args, **kwargs)
        self.disabled_choices = disabled_choices

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )

        if value in self.disabled_choices:
            option_dict['attrs']['disabled'] = 'disabled'
        return option_dict

class CreateCheckoutForm(forms.ModelForm):

    class Meta:
        model = Checkout
        fields = ['items', 'quantity', 'payment_currency', 'note']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields['payment_currency'].initial = settings.CHARGILY_DEFAULT_PAYMENT_CURRENCY
        self.fields['payment_currency'].empty_label = None
        self.fields['items'].empty_label = None

        for field in self.fields:
            ctx = {
                'placeholder': self.fields[field].label or field.title(),
            }
            # self.fields[field].label = ''

        queryset = self.fields['items'].queryset
        choices = self.fields['items'].choices
        disabled_choices = [obj.id for obj in queryset.exclude(is_active=True)]
        self.fields['items'].widget = SelectWidget(choices=choices, disabled_choices=disabled_choices)



    def clean(self):
        currency = self.cleaned_data.get('item')
        if currency and not currency.is_active:
            raise ValidationError(f"{currency.code} is inactive and cannot be selected.")
