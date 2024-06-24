from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from allauth.account.views import (
    SignupView, LoginView, LogoutView,
    ConfirmEmailView, EmailView, EmailVerificationSentView,
    PasswordResetView, PasswordSetView, PasswordChangeView,
    PasswordResetDoneView, PasswordResetFromKeyDoneView, PasswordResetFromKeyView
)

from allauth.account.views import send_email_confirmation

from .forms import RegistrationForm, AuthenticationForm


class RegistrationView(SignupView):
    template_name = 'apps/registrations/signup.html'
    model = get_user_model()
    form_class = RegistrationForm
    success_url = reverse_lazy('pages:home')

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

class AuthenticationView(LoginView):
    template_name = 'apps/registrations/login.html'
    model = get_user_model()
    form_class = AuthenticationForm
    success_url = reverse_lazy('pages:home')

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

class LoggingOutView(LogoutView):
    template_name = 'apps/registrations/logout.html'
    success_url = reverse_lazy('account_login')


class EmailChangeView(EmailView):
    template_name = 'apps/accounts/email/change.html'

    def form_invalid(self, form):
        if form.errors:
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

class EmailConfirmView(ConfirmEmailView):
    template_name = 'apps/accounts/email/confirm.html'

class EmailSentView(EmailVerificationSentView):
    template_name = "apps/accounts/email/sent.html"



class SetPasswordView(PasswordSetView):
    template_name = "apps/accounts/password/set.html"

class ChangePasswordView(PasswordChangeView):
    template_name = "apps/accounts/password/change.html"
    success_url = reverse_lazy('account_change_password_complete')

    def form_invalid(self, form):
        if form.errors.items():
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

class ChangePasswordCompleteView(TemplateView):
    template_name = "apps/accounts/password/complete.html"


class ResetPasswordView(PasswordResetView):
    template_name = "apps/accounts/password/reset.html"

    def form_invalid(self, form):
        if form.errors.items():
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)

class ResetPasswordSentView(PasswordResetDoneView):
    template_name = "apps/accounts/password/sent.html"


class ResetPasswordFormKeyView(PasswordResetFromKeyView):
    template_name = 'apps/accounts/password/reset_from_key.html'

    def form_invalid(self, form):
        if form.errors.items():
            for field, e in form.errors.items():
                error(self.request, e)
        return super().form_invalid(form)


class ResetPasswordFormKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = 'apps/accounts/password/reset_from_key_done.html'