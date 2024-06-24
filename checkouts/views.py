
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import View, ListView, DetailView, FormView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.messages import success, error
from django.utils.translation import gettext as _

from contrib.auth.decorators import owner_only, authenticated_only

from .models import Checkout
from .services import chargily_gateway, create_item_checkout, create_empty_checkout

# @method_decorator(owner_only, name='dispatch')
class CheckoutsView(ListView):
    template_name = 'apps/checkouts/checkouts.html'
    model = Checkout
    context_object_name = 'qs'

    def get_queryset(self):
        return self.model.objects.filter(customer=self.request.user)

# @method_decorator(owner_only, name='dispatch')
class CheckoutView(DetailView):
    template_name = 'apps/checkouts/checkout.html'
    model = Checkout
    context_object_name = 'object'

    def get_object(self):
        return get_object_or_404(
            self.model,
            customer=self.request.user,
            slug=self.kwargs.get('slug')
        )


class WebhookView(View):
    checkout_model = Checkout

    def post(self, request, *args, **kwargs):

        signature = request.headers.get("signature")
        payload = request.body.decode("utf-8")
        if not signature:
            return HttpResponse(status=400)

        if not chargily_gateway.validate_signature(signature, payload):
            return HttpResponse(status=403)

        event = json.loads(payload)

        checkout_id = event["data"]["id"]
        checkout = self.checkout_model.objects.get(chargily_entity_id=checkout_id)

        checkout_status = event["type"]
        if checkout_status == "checkout.paid": checkout.on_paid()
        elif checkout_status == "checkout.failed": checkout.on_failure()
        elif checkout_status == "checkout.canceled": checkout.on_cancel()
        elif checkout_status == "checkout.expired": checkout.on_expire()
        else: return HttpResponse(status=400)

        return JsonResponse({}, status=200)



