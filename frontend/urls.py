from django.urls import path

from .views import index, portal

urlpatterns = [
    path("", index),
    path("join", index),
    path("create", index),
    path("join/1", index),
    path("portal", portal),
]
