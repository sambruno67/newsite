from django.db import models
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel


# ══════════════════════════════════════════════════════════════════════
# Snippet : Projet
# ══════════════════════════════════════════════════════════════════════

@register_snippet
class Projet(models.Model):

    CATEGORIE_CHOICES = [
        ("gis",           "SIG & Cartographie"),
        ("teledetection", "Télédétection"),
        ("webmapping",    "Cartographie Web"),
        ("foncier",       "Foncier"),
        ("agriculture",   "Agriculture"),
        ("environnement", "Environnement"),
        ("autre",         "Autre"),
    ]

    # ── Contenu ───────────────────────────────────────────────────────
    titre              = models.CharField(max_length=255, verbose_name="Titre")
    slug               = models.SlugField(unique=True, blank=True)
    description_courte = models.TextField(verbose_name="Description courte", help_text="Affichée sur les cards.")
    description        = RichTextField(verbose_name="Description complète", blank=True)
    client             = models.CharField(max_length=200, blank=True, verbose_name="Client / Commanditaire")
    lieu               = models.CharField(max_length=200, blank=True, verbose_name="Lieu / Pays")

    # ── Classement ────────────────────────────────────────────────────
    categorie  = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default="gis", verbose_name="Catégorie")
    est_phare  = models.BooleanField(default=False, verbose_name="Projet phare", help_text="Affiche ce projet en grand en haut de la liste.")
    date       = models.DateField(verbose_name="Date de livraison")
    ordre      = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    # ── Médias ────────────────────────────────────────────────────────
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )
    emoji_fallback = models.CharField(
        max_length=4, blank=True, default="🗺️",
        verbose_name="Emoji (si pas d'image)",
    )

    # ── Stack technique ───────────────────────────────────────────────
    technologies = models.CharField(
        max_length=500, blank=True,
        verbose_name="Technologies (séparées par des virgules)",
        help_text="Ex : Django, PostGIS, Leaflet.js, QGIS",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("titre"),
            FieldPanel("slug"),
            FieldPanel("description_courte"),
            FieldPanel("description"),
        ], heading="Contenu"),
        MultiFieldPanel([
            FieldPanel("categorie"),
            FieldPanel("est_phare"),
            FieldPanel("date"),
            FieldPanel("ordre"),
        ], heading="Classement"),
        MultiFieldPanel([
            FieldPanel("client"),
            FieldPanel("lieu"),
            FieldPanel("technologies"),
        ], heading="Détails"),
        FieldPanel("image"),
        FieldPanel("emoji_fallback"),
    ]

    class Meta:
        verbose_name        = "Projet"
        verbose_name_plural = "Projets"
        ordering            = ["-date", "ordre"]

    def __str__(self):
        star = "⭐" if self.est_phare else "📁"
        return f"{star} {self.titre} ({self.date.year if self.date else '—'})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/projets/{self.slug}/"

    @property
    def tags_list(self):
        """Retourne la liste des technologies sous forme de liste."""
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(",") if t.strip()]

    @property
    def annee(self):
        return self.date.year if self.date else ""


# ══════════════════════════════════════════════════════════════════════
# Page Wagtail : liste des projets
# ══════════════════════════════════════════════════════════════════════

class ProjetsIndexPage(Page):
    """Page /projets/ — portfolio des réalisations."""

    intro = models.TextField(
        blank=True,
        verbose_name="Introduction",
        default=(
            "Du SIG foncier à la cartographie web, découvrez nos réalisations "
            "pour des institutions publiques, ONG et entreprises privées."
        ),
    )

    stat_projets    = models.PositiveIntegerField(default=50,  verbose_name="Projets livrés")
    stat_pays       = models.PositiveIntegerField(default=12,  verbose_name="Pays couverts")
    stat_clients    = models.PositiveIntegerField(default=30,  verbose_name="Clients satisfaits")
    stat_experience = models.PositiveIntegerField(default=8,   verbose_name="Années d'expérience")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([
            FieldPanel("stat_projets"),
            FieldPanel("stat_pays"),
            FieldPanel("stat_clients"),
            FieldPanel("stat_experience"),
        ], heading="Statistiques"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        categorie = request.GET.get("cat", "")
        qs = Projet.objects.all()
        if categorie:
            qs = qs.filter(categorie=categorie)

        context["projet_phare"]   = qs.filter(est_phare=True).first()
        context["projets"]        = qs.filter(est_phare=False).order_by("-date")
        context["categorie_active"] = categorie
        context["categories"]     = Projet.CATEGORIE_CHOICES

        return context

    class Meta:
        verbose_name = "Page Projets"
