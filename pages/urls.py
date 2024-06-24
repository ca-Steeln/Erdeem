
from django.urls import path

from .views import HomePageView, AboutPageView, BasePageView, Test403View

app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),

    path('base/', BasePageView.as_view(), name='base'),
    path('403/', Test403View.as_view(), name='403'),
]
