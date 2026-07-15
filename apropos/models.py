from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey


@register_snippet
class MembreEquipe(models.Model):
    """Géré via Snippets — Admin → Snippets → Membres"""
    initiales   = models.CharField(max_length=3, verbose_name="Initiales")
    nom         = models.CharField(max_length=100, verbose_name="Nom complet")
    poste       = models.CharField(max_length=150, verbose_name="Poste / rôle")
    competences = models.CharField(max_length=300, blank=True, verbose_name="Compétences (séparées par virgules)")
    couleur_bg  = models.CharField(max_length=100, blank=True, default="linear-gradient(135deg,#1A3A8F,#29ABE2)", verbose_name="Couleur avatar")
    ordre       = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    panels = [
        FieldPanel("initiales"),
        FieldPanel("nom"),
        FieldPanel("poste"),
        FieldPanel("competences"),
        FieldPanel("couleur_bg"),
        FieldPanel("ordre"),
    ]

    class Meta:
        verbose_name        = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering            = ["ordre"]

    def __str__(self):
        return self.nom

    @property
    def competences_list(self):
        return [c.strip() for c in self.competences.split(",") if c.strip()]


@register_snippet
class Partenaire(models.Model):
    """Géré via Snippets — Admin → Snippets → Partenaires"""
    emoji = models.CharField(max_length=4, blank=True, default="🏢")
    nom   = models.CharField(max_length=150, verbose_name="Nom")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    panels = [
        FieldPanel("emoji"),
        FieldPanel("nom"),
        FieldPanel("ordre"),
    ]

    class Meta:
        verbose_name        = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering            = ["ordre"]

    def __str__(self):
        return f"{self.emoji} {self.nom}"


@register_snippet
class EtapeTimeline(models.Model):
    """Géré via Snippets — Admin → Snippets → Timeline"""
    annee       = models.CharField(max_length=10, verbose_name="Année")
    titre       = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    est_actuel  = models.BooleanField(default=False, verbose_name="Étape actuelle")
    ordre       = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    panels = [
        FieldPanel("annee"),
        FieldPanel("titre"),
        FieldPanel("description"),
        FieldPanel("est_actuel"),
        FieldPanel("ordre"),
    ]

    class Meta:
        verbose_name        = "Étape timeline"
        verbose_name_plural = "Étapes timeline"
        ordering            = ["ordre"]

    def __str__(self):
        return f"{self.annee} — {self.titre}"


class AProposPage(Page):

    intro   = models.TextField(blank=True, default="Cabinet de consulting et de formation en géomatique basé à Ouagadougou, Burkina Faso.")
    mission = models.TextField(verbose_name="Mission", default="Fournir des solutions géospatiales innovantes et accessibles.")
    vision  = models.TextField(verbose_name="Vision", default="Être le cabinet de référence en géomatique en Afrique de l'Ouest.")
    valeurs = RichTextField(blank=True, verbose_name="Valeurs")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([
            FieldPanel("mission"),
            FieldPanel("vision"),
        ], heading="Mission & Vision"),
        FieldPanel("valeurs"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["membres"]          = MembreEquipe.objects.all()
        context["partenaires"]      = Partenaire.objects.all()
        context["timeline"]         = EtapeTimeline.objects.all()
        context["valeurs_statiques"] = _get_valeurs()
        return context

    class Meta:
        verbose_name = "Page À propos"


def _get_valeurs():
    return [
        {"emoji": "🎯", "titre": "Excellence",  "description": "Des livrables de haute qualité, validés terrain et documentés."},
        {"emoji": "🤝", "titre": "Proximité",   "description": "Un accompagnement personnalisé, ancré dans les réalités locales."},
        {"emoji": "🔓", "titre": "Open Source", "description": "Indépendance technologique grâce aux outils libres."},
        {"emoji": "📚", "titre": "Transfert",   "description": "Former pour autonomiser, pas pour créer des dépendances."},
    ]