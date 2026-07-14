from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey


# ══════════════════════════════════════════════════════════════════════
# Modèle de message reçu (stocké en base)
# ══════════════════════════════════════════════════════════════════════

class ContactMessage(models.Model):

    SUJET_CHOICES = [
        ("devis",          "Demande de devis"),
        ("formation",      "Formation"),
        ("partenariat",    "Partenariat"),
        ("renseignement",  "Renseignement"),
        ("autre",          "Autre"),
    ]

    sujet        = models.CharField(max_length=20, choices=SUJET_CHOICES, default="devis", verbose_name="Sujet")
    prenom       = models.CharField(max_length=100, verbose_name="Prénom")
    nom          = models.CharField(max_length=100, verbose_name="Nom")
    email        = models.EmailField(verbose_name="Email")
    telephone    = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    organisation = models.CharField(max_length=200, blank=True, verbose_name="Organisation")
    message      = models.TextField(verbose_name="Message")
    formation_ref = models.CharField(max_length=100, blank=True, verbose_name="Formation concernée (slug)")
    service_ref   = models.CharField(max_length=100, blank=True, verbose_name="Service concerné")

    lu           = models.BooleanField(default=False, verbose_name="Lu")
    created_at   = models.DateTimeField(auto_now_add=True, verbose_name="Reçu le")

    class Meta:
        verbose_name        = "Message reçu"
        verbose_name_plural = "Messages reçus"
        ordering            = ["-created_at"]

    def __str__(self):
        status = "✅" if self.lu else "🔔"
        return f"{status} {self.prenom} {self.nom} — {self.get_sujet_display()} ({self.created_at:%d/%m/%Y})"


# ══════════════════════════════════════════════════════════════════════
# Page Wagtail Contact
# ══════════════════════════════════════════════════════════════════════

class ContactPage(Page):
    """Page /contact/ — formulaire de contact."""

    intro = models.TextField(
        verbose_name="Introduction",
        blank=True,
        default="Une question, un projet ou une demande de devis ? Notre équipe vous répond sous 24h ouvrées.",
    )

    # Coordonnées
    adresse      = models.CharField(max_length=255, blank=True, default="Ouagadougou, Burkina Faso", verbose_name="Adresse")
    email_public = models.EmailField(blank=True, default="contact@innovgeomatic.com", verbose_name="Email public")
    telephone    = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    horaires     = models.TextField(
        blank=True,
        verbose_name="Horaires",
        default="Lun–Ven : 08h–17h | Sam : 09h–13h",
    )

    # Email de notification
    email_destinataire = models.EmailField(
        blank=True,
        default="contact@innovgeomatic.com",
        verbose_name="Email destinataire des messages",
        help_text="Adresse qui reçoit les notifications de nouveaux messages.",
    )

    # Réseaux sociaux
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn URL")
    twitter  = models.URLField(blank=True, verbose_name="Twitter/X URL")
    facebook = models.URLField(blank=True, verbose_name="Facebook URL")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([
            FieldPanel("adresse"),
            FieldPanel("email_public"),
            FieldPanel("telephone"),
            FieldPanel("horaires"),
            FieldPanel("email_destinataire"),
        ], heading="Coordonnées"),
        MultiFieldPanel([
            FieldPanel("linkedin"),
            FieldPanel("twitter"),
            FieldPanel("facebook"),
        ], heading="Réseaux sociaux"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        # Pré-remplissage depuis URL params (ex: /contact/?formation=qgis-fondamental)
        context["formation_ref"] = request.GET.get("formation", "")
        context["service_ref"]   = request.GET.get("service", "")
        context["sujet_init"]    = request.GET.get("sujet", "devis")
        # Message de succès après envoi
        context["success"] = request.GET.get("ok") == "1"
        return context

    class Meta:
        verbose_name = "Page Contact"
