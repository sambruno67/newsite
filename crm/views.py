from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Contact, Echange, Relance, Tag
from contact.models import ContactMessage

import csv
import io
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


def is_staff(user):
    return user.is_staff or user.is_superuser


# ══════════════════════════════════════════════════════════════════════
# Dashboard
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
def dashboard(request):
    aujourd_hui = timezone.now().date()
    ce_mois     = timezone.now().replace(day=1).date()

    # Stats globales
    stats = {
        "total_contacts":  Contact.objects.count(),
        "clients_actifs":  Contact.objects.filter(statut="client").count(),
        "devis_en_cours":  Contact.objects.filter(pipeline="devis").count(),
        "valeur_pipeline": Contact.objects.filter(
            pipeline__in=["devis", "negociation"]
        ).aggregate(total=Sum("valeur_devis"))["total"] or 0,
        "relances_a_faire": Relance.objects.filter(effectuee=False).count(),
        "nouveaux_ce_mois": Contact.objects.filter(created_at__date__gte=ce_mois).count(),
    }

    # Derniers contacts
    derniers_contacts = Contact.objects.order_by("-created_at")[:5]

    # Derniers échanges
    derniers_echanges = Echange.objects.select_related("contact").order_by("-date")[:5]

    # Relances urgentes
    relances_urgentes = Relance.objects.filter(
        effectuee=False,
        date_prevue__lte=aujourd_hui + timezone.timedelta(days=3)
    ).select_related("contact").order_by("date_prevue")[:5]

    # Répartition par tag
    tags_stats = Tag.objects.annotate(nb=Count("contact")).order_by("-nb")

    # Nouveaux messages non traités
    nouveaux_messages = ContactMessage.objects.filter(lu=False).order_by("-created_at")[:5]

    context = {
        "stats":             stats,
        "derniers_contacts": derniers_contacts,
        "derniers_echanges": derniers_echanges,
        "relances_urgentes": relances_urgentes,
        "tags_stats":        tags_stats,
        "nouveaux_messages": nouveaux_messages,
    }
    return render(request, "crm/dashboard.html", context)


# ══════════════════════════════════════════════════════════════════════
# Pipeline
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
def pipeline(request):
    etapes = Contact.PIPELINE_CHOICES
    colonnes = {}
    for code, label in etapes:
        colonnes[code] = {
            "label":    label,
            "contacts": Contact.objects.filter(pipeline=code).prefetch_related("tags"),
            "total":    Contact.objects.filter(pipeline=code).aggregate(
                            s=Sum("valeur_devis"))["s"] or 0,
            "count":    Contact.objects.filter(pipeline=code).count(),
        }
    return render(request, "crm/pipeline.html", {"colonnes": colonnes, "etapes": etapes})


# ══════════════════════════════════════════════════════════════════════
# Liste contacts
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
def liste_contacts(request):
    qs = Contact.objects.prefetch_related("tags").order_by("-created_at")

    # Filtres
    q       = request.GET.get("q", "")
    statut  = request.GET.get("statut", "")
    tag     = request.GET.get("tag", "")
    source  = request.GET.get("source", "")

    if q:
        qs = qs.filter(
            Q(nom__icontains=q) | Q(prenom__icontains=q) |
            Q(email__icontains=q) | Q(organisation__icontains=q)
        )
    if statut:
        qs = qs.filter(statut=statut)
    if tag:
        qs = qs.filter(tags__nom=tag)
    if source:
        qs = qs.filter(source=source)

    context = {
        "contacts":       qs,
        "tags":           Tag.objects.all(),
        "statut_choices": Contact.STATUT_CHOICES,
        "source_choices": Contact._meta.get_field("source").choices,
        "q":              q,
        "statut_actif":   statut,
        "tag_actif":      tag,
    }
    return render(request, "crm/liste_contacts.html", context)


# ══════════════════════════════════════════════════════════════════════
# Fiche contact
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
def fiche_contact(request, pk):
    contact  = get_object_or_404(Contact, pk=pk)
    echanges = contact.echanges.order_by("-date")
    relances = contact.relances.order_by("effectuee", "date_prevue")
    tags     = Tag.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_statut":
            contact.statut   = request.POST.get("statut", contact.statut)
            contact.pipeline = request.POST.get("pipeline", contact.pipeline)
            contact.notes    = request.POST.get("notes", contact.notes)
            contact.valeur_devis = request.POST.get("valeur_devis") or None
            contact.save()

        elif action == "add_echange":
            Echange.objects.create(
                contact=contact,
                type_echange=request.POST.get("type_echange", "note"),
                titre=request.POST.get("titre", ""),
                contenu=request.POST.get("contenu", ""),
                auteur=request.user,
            )

        elif action == "add_relance":
            Relance.objects.create(
                contact=contact,
                titre=request.POST.get("titre", ""),
                date_prevue=request.POST.get("date_prevue"),
                priorite=request.POST.get("priorite", "normale"),
                notes=request.POST.get("notes", ""),
            )

        elif action == "marquer_relance":
            relance_id = request.POST.get("relance_id")
            Relance.objects.filter(pk=relance_id, contact=contact).update(effectuee=True)

        return redirect("crm:fiche_contact", pk=pk)

    context = {
        "contact":  contact,
        "echanges": echanges,
        "relances": relances,
        "tags":     tags,
        "type_echange_choices": Echange.TYPE_CHOICES,
        "priorite_choices":     Relance.PRIORITE_CHOICES,
        "pipeline_choices":     Contact.PIPELINE_CHOICES,
        "statut_choices":       Contact.STATUT_CHOICES,
    }
    return render(request, "crm/fiche_contact.html", context)


# ══════════════════════════════════════════════════════════════════════
# Créer contact
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
def creer_contact(request):
    if request.method == "POST":
        contact = Contact.objects.create(
            prenom=request.POST.get("prenom", ""),
            nom=request.POST.get("nom", ""),
            email=request.POST.get("email", ""),
            telephone=request.POST.get("telephone", ""),
            organisation=request.POST.get("organisation", ""),
            lieu=request.POST.get("lieu", ""),
            poste=request.POST.get("poste", ""),
            statut=request.POST.get("statut", "nouveau"),
            pipeline=request.POST.get("pipeline", "nouveau"),
            source=request.POST.get("source", "autre"),
            notes=request.POST.get("notes", ""),
        )
        # Tags
        tag_ids = request.POST.getlist("tags")
        if tag_ids:
            contact.tags.set(tag_ids)

        return redirect("crm:fiche_contact", pk=contact.pk)

    context = {
        "tags":             Tag.objects.all(),
        "statut_choices":   Contact.STATUT_CHOICES,
        "pipeline_choices": Contact.PIPELINE_CHOICES,
        "source_choices":   Contact._meta.get_field("source").choices,
    }
    return render(request, "crm/creer_contact.html", context)


# ══════════════════════════════════════════════════════════════════════
# Importer depuis ContactMessage
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
@require_POST
def importer_message(request, message_id):
    """Convertit un message du formulaire contact en fiche CRM."""
    msg = get_object_or_404(ContactMessage, pk=message_id)

    # Vérifie si contact existe déjà
    contact, created = Contact.objects.get_or_create(
        email=msg.email,
        defaults={
            "prenom":       msg.prenom,
            "nom":          msg.nom,
            "telephone":    msg.telephone,
            "organisation": msg.organisation,
            "source":       "site",
            "statut":       "nouveau",
            "pipeline":     "nouveau",
        }
    )

    # Ajoute l'échange
    Echange.objects.create(
        contact=contact,
        type_echange="message",
        titre=f"Message site — {msg.get_sujet_display()}",
        contenu=msg.message,
        date=msg.created_at,
    )

    # Marque le message comme lu
    msg.lu = True
    msg.save()

    return redirect("crm:fiche_contact", pk=contact.pk)


# ══════════════════════════════════════════════════════════════════════
# Relances
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
def liste_relances(request):
    aujourd_hui = timezone.now().date()
    relances_a_faire = Relance.objects.filter(
        effectuee=False
    ).select_related("contact").order_by("date_prevue")

    relances_faites = Relance.objects.filter(
        effectuee=True
    ).select_related("contact").order_by("-date_prevue")[:20]

    context = {
        "relances_a_faire": relances_a_faire,
        "relances_faites":  relances_faites,
        "aujourd_hui":      aujourd_hui,
    }
    return render(request, "crm/relances.html", context)





# ══════════════════════════════════════════════════════════════════════
# Export CSV
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
def export_contacts_csv(request):
    """Exporte tous les contacts en CSV téléchargeable."""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="contacts_innov_geomatics.csv"'
    response.write("\ufeff")  # BOM pour Excel

    writer = csv.writer(response, delimiter=";")
    writer.writerow([
        "Prénom", "Nom", "Email", "Téléphone",
        "Organisation", "Poste", "Lieu",
        "Statut", "Pipeline", "Source",
        "Tags", "Valeur devis (FCFA)", "Notes",
        "Créé le",
    ])

    for c in Contact.objects.prefetch_related("tags").order_by("-created_at"):
        writer.writerow([
            c.prenom, c.nom, c.email, c.telephone,
            c.organisation, c.poste, c.lieu,
            c.get_statut_display(), c.get_pipeline_display(), c.get_source_display(),
            ", ".join(t.nom for t in c.tags.all()),
            c.valeur_devis or "",
            c.notes,
            c.created_at.strftime("%d/%m/%Y %H:%M"),
        ])

    return response


# ══════════════════════════════════════════════════════════════════════
# Import CSV
# ══════════════════════════════════════════════════════════════════════

@login_required
@user_passes_test(is_staff)
@require_http_methods(["GET", "POST"])
def import_contacts_csv(request):
    """Importe des contacts depuis un fichier CSV."""
    if request.method == "GET":
        return render(request, "crm/import_csv.html")

    fichier = request.FILES.get("fichier")
    if not fichier:
        return render(request, "crm/import_csv.html", {"erreur": "Aucun fichier sélectionné."})

    # Détecte l'encodage
    contenu = fichier.read()
    try:
        texte = contenu.decode("utf-8-sig")
    except UnicodeDecodeError:
        texte = contenu.decode("latin-1")

    reader = csv.DictReader(io.StringIO(texte), delimiter=";")

    crees   = 0
    ignores = 0
    erreurs = []

    # Mapping colonnes flexibles
    COLONNES = {
        "prenom":       ["Prénom", "prenom", "first_name", "firstname"],
        "nom":          ["Nom", "nom", "last_name", "lastname", "name"],
        "email":        ["Email", "email", "e-mail", "mail"],
        "telephone":    ["Téléphone", "telephone", "tel", "phone"],
        "organisation": ["Organisation", "organisation", "org", "company", "société"],
        "poste":        ["Poste", "poste", "fonction", "title", "job"],
        "lieu":         ["Lieu", "lieu", "pays", "city", "ville", "country"],
        "notes":        ["Notes", "notes", "remarques", "comments"],
    }

    def get_val(row, champ):
        for col in COLONNES.get(champ, []):
            if col in row:
                return row[col].strip()
        return ""

    for i, row in enumerate(reader, start=2):
        try:
            nom = get_val(row, "nom")
            if not nom:
                ignores += 1
                continue

            email = get_val(row, "email")

            # Évite les doublons par email
            if email and Contact.objects.filter(email=email).exists():
                ignores += 1
                continue

            Contact.objects.create(
                prenom=get_val(row, "prenom"),
                nom=nom,
                email=email,
                telephone=get_val(row, "telephone"),
                organisation=get_val(row, "organisation"),
                poste=get_val(row, "poste"),
                lieu=get_val(row, "lieu"),
                notes=get_val(row, "notes"),
                source="autre",
                statut="nouveau",
                pipeline="nouveau",
            )
            crees += 1

        except Exception as e:
            erreurs.append(f"Ligne {i} : {e}")

    context = {
        "succes": True,
        "crees":   crees,
        "ignores": ignores,
        "erreurs": erreurs,
    }
    return render(request, "crm/import_csv.html", context)