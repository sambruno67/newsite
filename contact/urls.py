from django.urls import path
from . import views

urlpatterns = [
    path("contact/envoyer/", views.contact_submit, name="contact_submit"),
]
