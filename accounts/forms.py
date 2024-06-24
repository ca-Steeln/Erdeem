
from phonenumber_field.formfields import PhoneNumberField

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Account


# * Account Settings --------------------

class AccountSettingsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)

    def clean(self):
        print(self.cleaned_data)
        return super().clean()

class SecuritySettingsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)

class PaymentSettingsForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)

# * Profile Settings --------------------
class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'avatar', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)

# * Preferences Settings -----------------
class ThemeSettingsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['theme']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)

        theme_choices = self.fields['theme'].choices
        self.fields['theme'].widget = forms.RadioSelect(choices=theme_choices)

class LocaleSettingsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['locale']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)

class NotificationSettingsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            ctx = {
                # html element attributes
                'placeholder': self.fields[field].label or field.title(),
            }

            self.fields[field].widget.attrs.update(ctx)
