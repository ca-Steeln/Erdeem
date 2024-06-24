
from functools import wraps

from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages import error, success
from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import DisallowedRedirect
from django.utils.translation import gettext as _

from contrib.auth import USER_MODEL



def staff_only(view):
    @wraps(view)
    @login_required
    def wrapped_view(request, *args, **kwargs):
        get_object_or_404(USER_MODEL, pk=request.user.pk, is_staff=True)
        return view(request, *args, **kwargs)
    return wrapped_view

# * Beta *
def owner_only(view, model):
    """ Beta: Authenticated Owner user only could access """
    @wraps(view)
    @login_required
    def wrapped_view(request, *args, **kwargs):
        get_object_or_404(model, member=request.user, **kwargs)
        return view(request, *args, **kwargs)
    return wrapped_view

def authenticated_only(view):
    """ Authenticated users only could access """
    @wraps(view)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if settings.DEBUG:
                raise DisallowedRedirect('Decorator Error: 401 Error User is not authenticated')
            error(request, _('Authentication required, please login to access the request destination!)'))
            # ! Redirect user to login page
            return HttpResponse(status_code=401)
        return view(request, *args, **kwargs)
    return wrapped_view

def anonymous_only(view):
    """ Anonymous users only could access """
    @wraps(view)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_anonymous:
            if settings.DEBUG:
                raise DisallowedRedirect('Decorator Error: 401 Error User is not anonymous')
            error(request, _('Access is not permitted to this destination!'))
            return HttpResponse(status_code=401)
        return view(request, *args, **kwargs)
    return wrapped_view


def under_construction(view):
    """ Used for a temporarily unavailable view for normal users and not staff. """
    @wraps(view)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            error(request, _('The section is under construction, please try again later.'))
            return HttpResponse(status=503)
        return view(request, *args, **kwargs)
    return wrapped_view