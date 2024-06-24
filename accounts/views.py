
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.conf import settings

from contrib.auth.decorators import authenticated_only
from .models import Account


# Create your views here.

@method_decorator(authenticated_only, name='dispatch')
class ProfileView(DetailView):
    template_name = 'apps/accounts/profile.html'
    model = Account
    context_object_name = 'object'

    def get_object(self):
        return get_object_or_404(
            self.model,
            slug = self.kwargs.get('slug'),
        )


