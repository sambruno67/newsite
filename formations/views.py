from django.shortcuts import get_object_or_404, render
from .models import Formation


def formation_detail(request, slug):
    """Page détail d'une formation avec programme, TDR, formateurs, documents."""
    formation = get_object_or_404(Formation, slug=slug)

    # Formations similaires
    similaires = Formation.objects.filter(
        categorie=formation.categorie,
        est_disponible=True,
    ).exclude(pk=formation.pk)[:3]

    context = {
        "formation": formation,
        "similaires": similaires,
    }
    return render(request, "formations/formation_detail.html", context)
