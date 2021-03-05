from django.urls import path
from .views import VditorImagesUploadView


urlpatterns = [
    path('uploads/', VditorImagesUploadView, name='uploads')
]