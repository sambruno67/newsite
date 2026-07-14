from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import ContactMessage


@require_POST
def contact_submit(request):
    """
    Traite la soumission du formulaire de contact.
    Enregistre le message en base et envoie un email de notification.
    Redirige vers /contact/?ok=1 en cas de succès.
    """
    sujet        = request.POST.get("sujet", "autre")
    prenom       = request.POST.get("prenom", "").strip()
    nom          = request.POST.get("nom", "").strip()
    email        = request.POST.get("email", "").strip()
    telephone    = request.POST.get("telephone", "").strip()
    organisation = request.POST.get("organisation", "").strip()
    message_text = request.POST.get("message", "").strip()
    formation_ref = request.POST.get("formation_ref", "").strip()
    service_ref   = request.POST.get("service_ref", "").strip()
    rgpd          = request.POST.get("rgpd", "")

    # Validation minimale
    if not all([prenom, nom, email, message_text, rgpd]):
        return redirect("/contact/?erreur=champs_manquants")

    # Sauvegarde en base
    msg = ContactMessage.objects.create(
        sujet=sujet,
        prenom=prenom,
        nom=nom,
        email=email,
        telephone=telephone,
        organisation=organisation,
        message=message_text,
        formation_ref=formation_ref,
        service_ref=service_ref,
    )

    # Email de notification (silencieux si SMTP non configuré)
    try:
        destinataire = getattr(settings, "CONTACT_EMAIL", "contact@innovgeomatic.com")
        sujet_map = {
            "devis": "Demande de devis",
            "formation": "Formation",
            "partenariat": "Partenariat",
            "renseignement": "Renseignement",
            "autre": "Autre",
        }
        send_mail(
            subject=f"[Innov Geomatics] {sujet_map.get(sujet, sujet)} — {prenom} {nom}",
            message=(
                f"Nouveau message reçu sur innovgeomatic.com\n\n"
                f"Sujet      : {sujet_map.get(sujet, sujet)}\n"
                f"Nom        : {prenom} {nom}\n"
                f"Email      : {email}\n"
                f"Téléphone  : {telephone or '—'}\n"
                f"Structure  : {organisation or '—'}\n"
                f"Formation  : {formation_ref or '—'}\n"
                f"Service    : {service_ref or '—'}\n\n"
                f"Message :\n{message_text}\n\n"
                f"---\nID message : #{msg.pk}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[destinataire],
            fail_silently=True,
        )
    except Exception:
        pass  # Ne pas bloquer si email non configuré

    return redirect("/contact/?ok=1")
