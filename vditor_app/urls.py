from django.urls import path
from .views import vditor_form_view


urlpatterns = [
    path("", vditor_form_view, name="vditor_form"),
]
