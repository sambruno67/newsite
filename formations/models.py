from django.db import models
from django.utils.text import slugify
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# ══════════════════════════════════════════════════════════════════════
# Snippet : Formation (géré via Wagtail Snippets)
# ══════════════════════════════════════════════════════════════════════

class ModuleFormation(Orderable):
    """Module / point du programme d'une formation."""
    formation = ParentalKey(
        "Formation",
        on_delete=models.CASCADE,
        related_name="modules",
    )
    titre = models.CharField(max_length=255, verbose_name="Intitulé du module")

    panels = [FieldPanel("titre")]

    class Meta(Orderable.Meta):
        verbose_name = "Module"

    def __str__(self):
        return self.titre


@register_snippet
class Formation(ClusterableModel):
    """
    Formation géomatique — gérée comme Snippet Wagtail.
    Apparaît dans le menu Snippets > Formations de l'admin.
    """

    CATEGORIE_CHOICES = [
        ("gis",           "SIG & QGIS"),
        ("teledetection", "Télédétection"),
        ("webmapping",    "Cartographie Web"),
        ("collecte",      "Collecte de données"),
        ("autre",         "Autre"),
    ]

    MODALITE_CHOICES = [
        ("presentiel", "Présentiel"),
        ("enligne",    "En ligne"),
        ("hybride",    "Hybride"),
    ]

    # ── Infos principales ─────────────────────────────────────────────
    titre              = models.CharField(max_length=255, verbose_name="Titre")
    slug               = models.SlugField(unique=True, blank=True, verbose_name="Slug URL")
    description_courte = models.TextField(verbose_name="Description courte", help_text="Affichée sur les cards.")
    description        = RichTextField(verbose_name="Description complète", blank=True)

    # ── Statut ────────────────────────────────────────────────────────
    est_disponible = models.BooleanField(
        default=False,
        verbose_name="Disponible à l'inscription",
        help_text="Cocher pour afficher le bouton 'S'inscrire' et le badge 'Disponible'.",
    )
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIE_CHOICES,
        default="gis",
        verbose_name="Catégorie",
    )
    modalite = models.CharField(
        max_length=12,
        choices=MODALITE_CHOICES,
        default="presentiel",
        verbose_name="Modalité",
    )

    # ── Détails pratiques ─────────────────────────────────────────────
    duree           = models.CharField(max_length=60,  blank=True, verbose_name="Durée (ex : 5 jours)")
    nb_participants = models.CharField(max_length=60,  blank=True, verbose_name="Participants (ex : 8–15 pers.)")
    lieu            = models.CharField(max_length=120, blank=True, verbose_name="Lieu")
    prix            = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Prix (FCFA)",
        help_text="Laisser vide si le prix n'est pas encore défini.",
    )

    # ── Ordre & image ────────────────────────────────────────────────
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de couverture",
    )

    # ── Timestamps ────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ── Admin panels ──────────────────────────────────────────────────
    panels = [
        MultiFieldPanel([
            FieldPanel("titre"),
            FieldPanel("slug"),
            FieldPanel("description_courte"),
            FieldPanel("description"),
        ], heading="Contenu"),
        MultiFieldPanel([
            FieldPanel("est_disponible"),
            FieldPanel("categorie"),
            FieldPanel("modalite"),
        ], heading="Statut & catégorie"),
        MultiFieldPanel([
            FieldPanel("duree"),
            FieldPanel("nb_participants"),
            FieldPanel("lieu"),
            FieldPanel("prix"),
            FieldPanel("ordre"),
        ], heading="Infos pratiques"),
        FieldPanel("image"),
        InlinePanel("modules", label="Module du programme"),
    ]

    class Meta:
        verbose_name        = "Formation"
        verbose_name_plural = "Formations"
        ordering            = ["ordre", "titre"]

    def __str__(self):
        status = "✅" if self.est_disponible else "🔜"
        return f"{status} {self.titre}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/formations/{self.slug}/"

    @property
    def prix_display(self):
        if self.prix:
            return f"{self.prix:,} FCFA".replace(",", " ")
        return "Prix à définir"


# ══════════════════════════════════════════════════════════════════════
# Page Wagtail : liste des formations
# ══════════════════════════════════════════════════════════════════════

class FormationsIndexPage(Page):
    """Page /formations/ — liste toutes les formations."""

    intro = models.TextField(
        verbose_name="Introduction",
        blank=True,
        default=(
            "Des programmes pratiques animés par des experts terrain, "
            "en présentiel à Ouagadougou ou en ligne. Certifiés et adaptés au contexte africain."
        ),
    )
    stat_formes    = models.PositiveIntegerField(default=200, verbose_name="Professionnels formés")
    stat_programmes = models.PositiveIntegerField(default=8,   verbose_name="Nombre de programmes")
    stat_satisfaction = models.PositiveIntegerField(default=95, verbose_name="Taux de satisfaction (%)")

    lms_url = models.URLField(
        blank=True,
        default="https://learn.innovgeomatic.com",
        verbose_name="URL plateforme LMS",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([
            FieldPanel("stat_formes"),
            FieldPanel("stat_programmes"),
            FieldPanel("stat_satisfaction"),
        ], heading="Statistiques hero"),
        FieldPanel("lms_url"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Filtre par catégorie si paramètre GET
        categorie = request.GET.get("cat", "")
        modalite  = request.GET.get("mode", "")

        qs = Formation.objects.all().order_by("ordre", "titre")
        if categorie:
            qs = qs.filter(categorie=categorie)
        if modalite:
            qs = qs.filter(modalite=modalite)

        context["formations_dispo"]  = qs.filter(est_disponible=True)
        context["formations_coming"] = qs.filter(est_disponible=False)
        context["categorie_active"]  = categorie
        context["modalite_active"]   = modalite
        context["categories"]        = Formation.CATEGORIE_CHOICES
        context["modalites"]         = Formation.MODALITE_CHOICES

        return context

    class Meta:
        verbose_name = "Page Formations"
