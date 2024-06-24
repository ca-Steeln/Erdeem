
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render


# Create your views here.

def csrf_handler403_view(request, reason="", *args, **kwargs):
    response = render(request, 'handlers/csrf_403.html')
    response.status_code = 403
    return response

def handler403_view(request, *args, **kwargs):
    response = render(request, 'handlers/403.html')
    response.status_code = 403
    return response

def handler404_view(request, *args, **kwargs):
    response = render(request, 'handlers/404.html')
    response.status_code = 404
    return response

