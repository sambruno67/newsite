from django.shortcuts import get_object_or_404, render
from .models import Projet

def projet_detail(request, slug):
    projet = get_object_or_404(Projet, slug=slug)
    return render(request, "projets/projet_detail.html", {"projet": projet})
