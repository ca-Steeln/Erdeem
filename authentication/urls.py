
from django.urls import path, re_path
from .views import (
    RegistrationView, AuthenticationView, LoggingOutView,
    EmailConfirmView, EmailChangeView, EmailSentView,
    ResetPasswordView, SetPasswordView, ChangePasswordView, ChangePasswordCompleteView, ResetPasswordSentView,
    ResetPasswordFormKeyView, ResetPasswordFormKeyDoneView,
)

urlpatterns = [

    path('sign-up/', RegistrationView.as_view(), name='account_signup'),
    path('sign-in/', AuthenticationView.as_view(), name='account_login'),
    path('sign-out/', LoggingOutView.as_view(), name='account_logout'),

    # ? Changing email needs a more secure process | settings.ACCOUNT_CHANGE_EMAIL is False
    # path('settings/security/email-change/', EmailChangeView.as_view(), name='account_email'),

    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", EmailConfirmView.as_view(), name='account_confirm_email'),
    path('email-sent/', EmailSentView.as_view(), name='account_email_verification_sent'),

    path('password-reset/', ResetPasswordView.as_view(), name='account_reset_password'),
    path('password-reset-sent/', ResetPasswordSentView.as_view(), name='account_reset_password_done'),
    path('password-set/', SetPasswordView.as_view(), name='account_set_password'),
    path('settings/security/password-change/', ChangePasswordView.as_view(), name='account_change_password'),
    path('password-change-complete/', ChangePasswordCompleteView.as_view(), name='account_change_password_complete'),

    re_path(r"^password-reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", ResetPasswordFormKeyView.as_view(), name='account_reset_password_from_key'),
    path('password-reset-done/', ResetPasswordFormKeyDoneView.as_view(), name='account_reset_password_from_key_done'),
]
