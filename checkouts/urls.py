
from django.urls import path
from .views import WebhookView, CheckoutsView, CheckoutView


app_name = 'checkouts'

urlpatterns = [
    path('', CheckoutsView.as_view(), name="checkouts"),
    path('<slug:slug>/', CheckoutView.as_view(), name="checkout"),

    path('webhook/', WebhookView.as_view(), name="webhook"),
]
