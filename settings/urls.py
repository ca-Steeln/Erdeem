
from django.urls import path
from .views import (
    SettingsView,
    AccountSettingsView, SecuritySettingsView, PaymentSettingsView,
    ProfileSettingsView, PrivacySettingsView,
    ThemeSettingsView, LocaleSettingsView, NotificationSettingsView
)

app_name = 'settings'

urlpatterns = [
    path('', SettingsView.as_view(), name='settings'),
    path('account/', AccountSettingsView.as_view(), name='account'),
    path('security/', SecuritySettingsView.as_view(), name='security'),
    path('payments/', PaymentSettingsView.as_view(), name='payments'),

    path('profile/', ProfileSettingsView.as_view(), name='profile'),
    path('privacy/', PrivacySettingsView.as_view(), name='privacy'),

    path('theme/', ThemeSettingsView.as_view(), name='theme'),
    path('languages/', LocaleSettingsView.as_view(), name='locale'),
    path('notifications/', NotificationSettingsView.as_view(), name='notifications'),

]