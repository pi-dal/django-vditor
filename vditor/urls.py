from django.urls import path
from .views import vditor_images_upload_view


urlpatterns = [path("uploads/", vditor_images_upload_view, name="uploads")]
