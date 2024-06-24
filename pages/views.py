
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages import success, error
from django.urls import reverse
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import TemplateView, View
from django.core.exceptions import PermissionDenied



# Create your views here.

class HomePageView(TemplateView):
    template_name = 'apps/pages/home.html'

    def post(self, request):
        success(self.request, 'test')
        return render(request, self.template_name)

class AboutPageView(TemplateView):
    template_name = 'apps/pages/about.html'

# ! staff only decorator needed
class BasePageView(TemplateView):
    template_name = 'base/base.html'

# ! staff only decorator needed
class Test403View(View):
    def get(self, request):
        raise PermissionDenied

