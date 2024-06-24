
from django.urls import path
from .views import ProfileView

app_name = 'accounts'

urlpatterns = [

    path('<slug:slug>/', ProfileView.as_view(), name='profile'),
]