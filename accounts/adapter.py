
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import FieldDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site

from allauth.core import context
from allauth import app_settings as allauth_app_settings
from allauth.account import signals
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account import app_settings


class AccountAdapter(DefaultAccountAdapter):

    DefaultAccountAdapter.error_messages.update({
    "account_inactive": _("This account is currently inactive."),
    "email_password_mismatch": _("The email address or password you specified is incorrect."),
    "username_password_mismatch": _("The username or password you specified is incorrect."),
    "email_taken": _("Someone is already registered with this email address."),
    "username_taken": _("Someone is already registered with this username."),
    })

    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Renders an email to `email`.  `template_prefix` identifies the
        email that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        bodies = {}
        html_ext = app_settings.TEMPLATE_EXTENSION

        try:
            template_name = "{0}_message.{1}".format(template_prefix, html_ext)
            bodies[html_ext] = render_to_string(
                template_name,
                context,
                globals()["context"].request,
            ).strip()
        except TemplateDoesNotExist:
            if not bodies:
                # We need at least one body
                raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, headers=headers
            )
            if html_ext in bodies:
                msg.attach_alternative(bodies[html_ext], "text/html")
        else:
            msg = EmailMessage(
                subject, bodies[html_ext], from_email, to, headers=headers
            )
            msg.content_subtype = "html"  # Main content is now text/html
        return msg


    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = "apps/accounts/email/confirmation_signup"
        else:
            email_template = "apps/accounts/email/confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)