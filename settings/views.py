

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, DetailView, UpdateView, TemplateView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.conf import settings

from allauth.account.views import EmailView, PasswordChangeView

from contrib.auth.decorators import authenticated_only
from accounts.models import Account

from accounts.forms import (
    AccountSettingsForm, SecuritySettingsForm, PaymentSettingsForm,
    ProfileSettingsForm, PrivacySettingsForm,
    ThemeSettingsForm, LocaleSettingsForm, NotificationSettingsForm
)

# Create your views here.


# * Settings ----------------------------

@method_decorator(authenticated_only, name='dispatch')
class SettingsView(TemplateView):
    template_name = 'apps/settings/settings.html'



# * Account Settings --------------------

@method_decorator(authenticated_only, name='dispatch')
class AccountSettingsView(UpdateView):
    template_name = 'apps/settings/account.html'
    model = Account
    form_class = AccountSettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

@method_decorator(authenticated_only, name='dispatch')
class SecuritySettingsView(UpdateView):
    template_name = 'apps/settings/security.html'
    model = Account
    form_class = SecuritySettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

@method_decorator(authenticated_only, name='dispatch')
class PaymentSettingsView(UpdateView):
    template_name = 'apps/settings/payments.html'
    model = Account
    form_class = PaymentSettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

class EmailChangeView(EmailView):
    template_name = 'apps/accounts/email/change.html'

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

class ChangePasswordView(PasswordChangeView):
    template_name = "apps/accounts/password/change.html"
    success_url = reverse_lazy('account_change_password_complete')

    def form_invalid(self, form):
        if form.errors.items():
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

# * Profile Settings --------------------

@method_decorator(authenticated_only, name='dispatch')
class ProfileSettingsView(UpdateView):
    template_name = 'apps/settings/profile.html'
    model = Account
    form_class = ProfileSettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

@method_decorator(authenticated_only, name='dispatch')
class PrivacySettingsView(UpdateView):
    template_name = 'apps/settings/privacy.html'
    model = Account
    form_class = PrivacySettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)



# * Preferences Settings -----------------

@method_decorator(authenticated_only, name='dispatch')
class ThemeSettingsView(UpdateView):
    template_name = 'apps/settings/theme.html'
    model = Account
    form_class = ThemeSettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

@method_decorator(authenticated_only, name='dispatch')
class LocaleSettingsView(UpdateView):
    template_name = 'apps/settings/locale.html'
    model = Account
    form_class = LocaleSettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

@method_decorator(authenticated_only, name='dispatch')
class NotificationSettingsView(UpdateView):
    template_name = 'apps/settings/notifications.html'
    model = Account
    form_class = NotificationSettingsForm

    def get_object(self):
        return get_object_or_404(
            self.model,
            member=self.request.user
        )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)


# * Community and Policies ---------------