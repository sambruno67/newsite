from django.urls import path
from . import views

urlpatterns = [
    path("projets/<slug:slug>/", views.projet_detail, name="projet_detail"),
]