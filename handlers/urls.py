
from django.conf.urls import handler403, handler404
from handlers.views import handler403_view, handler404_view

handler403 = handler403_view
handler404 = handler404_view
