from django.urls import path
from .views import get_location, Example

app_name='locations'

urlpatterns = [
    path('ajax/get_location', get_location, name='ajax_get_location'),
    path('home', Example.as_view()),
]
