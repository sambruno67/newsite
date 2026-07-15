from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# ══════════════════════════════════════════════════════════════════════
# Membres de l'équipe (Orderable inline)
# ══════════════════════════════════════════════════════════════════════

class MembreEquipe(Orderable):
    page       = ParentalKey("AProposPage", related_name="membres", on_delete=models.CASCADE)
    initiales  = models.CharField(max_length=3, verbose_name="Initiales (ex: BW)")
    nom        = models.CharField(max_length=100, verbose_name="Nom complet")
    poste      = models.CharField(max_length=150, verbose_name="Poste / rôle")
    competences = models.CharField(
        max_length=300, blank=True,
        verbose_name="Compétences (séparées par des virgules)",
        help_text="Ex : SIG, Django, WebMapping",
    )
    couleur_bg = models.CharField(
        max_length=100, blank=True,
        default="linear-gradient(135deg,#1A3A8F,#29ABE2)",
        verbose_name="Couleur de fond avatar (CSS gradient ou hex)",
    )

    panels = [
        FieldPanel("initiales"),
        FieldPanel("nom"),
        FieldPanel("poste"),
        FieldPanel("competences"),
        FieldPanel("couleur_bg"),
    ]

    @property
    def competences_list(self):
        return [c.strip() for c in self.competences.split(",") if c.strip()]


# ══════════════════════════════════════════════════════════════════════
# Étapes de la timeline (Orderable inline)
# ══════════════════════════════════════════════════════════════════════

class EtapeTimeline(Orderable):
    page        = ParentalKey("AProposPage", related_name="timeline", on_delete=models.CASCADE)
    annee       = models.CharField(max_length=10, verbose_name="Année")
    titre       = models.CharField(max_length=200, verbose_name="Titre de l'étape")
    description = models.TextField(verbose_name="Description")
    est_actuel  = models.BooleanField(default=False, verbose_name="Étape actuelle (couleur navy)")

    panels = [
        FieldPanel("annee"),
        FieldPanel("titre"),
        FieldPanel("description"),
        FieldPanel("est_actuel"),
    ]


# ══════════════════════════════════════════════════════════════════════
# Partenaires (Orderable inline)
# ══════════════════════════════════════════════════════════════════════

class Partenaire(Orderable):
    page  = ParentalKey("AProposPage", related_name="partenaires", on_delete=models.CASCADE)
    emoji = models.CharField(max_length=4, blank=True, default="🏢", verbose_name="Emoji")
    nom   = models.CharField(max_length=150, verbose_name="Nom du partenaire")

    panels = [
        FieldPanel("emoji"),
        FieldPanel("nom"),
    ]


# ══════════════════════════════════════════════════════════════════════
# Page À propos (Wagtail Page)
# ══════════════════════════════════════════════════════════════════════

class AProposPage(Page):
    """Page /a-propos/ — présentation d'Innov Geomatics."""

    # ── Intro ────────────────────────────────────────────────────────
    intro = models.TextField(
        blank=True,
        verbose_name="Introduction",
        default=(
            "Cabinet de consulting et de formation en géomatique basé à Ouagadougou, "
            "Burkina Faso. Nous mettons l'expertise géospatiale au service du développement durable en Afrique."
        ),
    )

    # ── Mission & Vision ─────────────────────────────────────────────
    mission = models.TextField(
        verbose_name="Mission",
        default=(
            "Fournir des solutions géospatiales innovantes et accessibles qui permettent "
            "aux organisations africaines de prendre des décisions éclairées basées sur la donnée territoriale."
        ),
    )
    vision = models.TextField(
        verbose_name="Vision",
        default=(
            "Être le cabinet de référence en géomatique en Afrique de l'Ouest, reconnu pour "
            "l'excellence technique, le transfert de compétences et l'impact sur le développement local."
        ),
    )

    # ── Valeurs ──────────────────────────────────────────────────────
    valeurs = RichTextField(
        blank=True,
        verbose_name="Valeurs (texte riche)",
        help_text="Utilisé comme fallback si les valeurs statiques ne conviennent pas.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([
            FieldPanel("mission"),
            FieldPanel("vision"),
        ], heading="Mission & Vision"),
        InlinePanel("timeline", label="Étape de la timeline"),
        InlinePanel("membres", label="Membre de l'équipe"),
        InlinePanel("partenaires", label="Partenaire / client"),
        FieldPanel("valeurs"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["valeurs_statiques"] = _get_valeurs()
        return context

    class Meta:
        verbose_name = "Page À propos"


# ── Données statiques valeurs ──────────────────────────────────────────

def _get_valeurs():
    return [
        {"emoji": "🎯", "titre": "Excellence",  "description": "Des livrables de haute qualité, validés terrain et documentés."},
        {"emoji": "🤝", "titre": "Proximité",   "description": "Un accompagnement personnalisé, ancré dans les réalités locales."},
        {"emoji": "🔓", "titre": "Open Source", "description": "Indépendance technologique grâce aux outils libres."},
        {"emoji": "📚", "titre": "Transfert",   "description": "Former pour autonomiser, pas pour créer des dépendances."},
    ]
