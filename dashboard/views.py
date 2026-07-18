from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Count, Sum, Q


def is_staff(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff)
def dashboard(request):
    aujourd_hui = timezone.now().date()
    ce_mois     = timezone.now().replace(day=1).date()

    # ── CRM stats ─────────────────────────────────────────────────────
    crm_stats = {}
    try:
        from crm.models import Contact, Relance
        crm_stats = {
            "total_contacts":   Contact.objects.count(),
            "nouveaux_ce_mois": Contact.objects.filter(created_at__date__gte=ce_mois).count(),
            "clients":          Contact.objects.filter(statut="client").count(),
            "devis_en_cours":   Contact.objects.filter(pipeline="devis").count(),
            "valeur_pipeline":  Contact.objects.filter(
                pipeline__in=["devis","negociation"]
            ).aggregate(t=Sum("valeur_devis"))["t"] or 0,
            "relances_total":   Relance.objects.filter(effectuee=False).count(),
            "relances_retard":  Relance.objects.filter(
                effectuee=False, date_prevue__lt=aujourd_hui
            ).count(),
        }
        # Pipeline
        pipeline_data = []
        for code, label in Contact.PIPELINE_CHOICES:
            cnt = Contact.objects.filter(pipeline=code).count()
            pipeline_data.append({"code": code, "label": label, "count": cnt})
        crm_stats["pipeline"] = pipeline_data

        # Relances urgentes
        crm_stats["relances_urgentes"] = Relance.objects.filter(
            effectuee=False
        ).select_related("contact").order_by("date_prevue")[:5]

    except Exception:
        pass

    # ── Messages contact ───────────────────────────────────────────────
    messages_recus = []
    nb_messages_non_lus = 0
    try:
        from contact.models import ContactMessage
        messages_recus       = ContactMessage.objects.order_by("-created_at")[:5]
        nb_messages_non_lus  = ContactMessage.objects.filter(lu=False).count()
    except Exception:
        pass

    # ── Wagtail pages ─────────────────────────────────────────────────
    pages_info = []
    try:
        from wagtail.models import Page
        pages = Page.objects.filter(depth__gt=2).order_by("-last_published_at")[:8]
        pages_info = pages
    except Exception:
        pass

    # ── Contenu stats ─────────────────────────────────────────────────
    contenu = {}
    try:
        from projets.models import Projet
        contenu["projets"] = Projet.objects.count()
    except Exception:
        contenu["projets"] = 0
    try:
        from formations.models import Formation
        contenu["formations"] = Formation.objects.count()
        contenu["formations_dispo"] = Formation.objects.filter(est_disponible=True).count()
    except Exception:
        contenu["formations"] = 0
        contenu["formations_dispo"] = 0
    try:
        from blog.models import BlogPost
        contenu["articles"] = BlogPost.objects.live().count()
    except Exception:
        contenu["articles"] = 0
    try:
        from apropos.models import MembreEquipe, Partenaire
        contenu["membres"]     = MembreEquipe.objects.count()
        contenu["partenaires"] = Partenaire.objects.count()
    except Exception:
        contenu["membres"]     = 0
        contenu["partenaires"] = 0

    # ── Activité récente ──────────────────────────────────────────────
    activites = []
    try:
        from crm.models import Echange
        for e in Echange.objects.select_related("contact").order_by("-date")[:5]:
            activites.append({
                "texte": f"{e.get_type_echange_display()} — {e.contact.nom_complet}",
                "date":  e.date,
                "type":  "crm",
            })
    except Exception:
        pass

    context = {
        "crm_stats":            crm_stats,
        "messages_recus":       messages_recus,
        "nb_messages_non_lus":  nb_messages_non_lus,
        "pages_info":           pages_info,
        "contenu":              contenu,
        "activites":            activites,
        "aujourd_hui":          aujourd_hui,
        "user":                 request.user,
    }
    return render(request, "dashboard/dashboard.html", context)
