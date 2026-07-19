from django.urls import path
from . import views

urlpatterns = [
    path("formations/<slug:slug>/", views.formation_detail, name="formation_detail"),
]
