from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey


# ── Livrable d'un service ──────────────────────────────────────────────────────
class ServiceLivrable(Orderable):
    page   = ParentalKey("ServicesIndexPage", related_name="livrables", on_delete=models.CASCADE)
    service = models.CharField(
        max_length=20,
        choices=[
            ("gis",         "SIG & Cartographie"),
            ("teledetection", "Télédétection"),
            ("webmapping",  "Cartographie Web"),
            ("conseil",     "Conseil & Expertise"),
        ],
        verbose_name="Service concerné",
    )
    texte = models.CharField(max_length=200, verbose_name="Livrable")

    panels = [
        FieldPanel("service"),
        FieldPanel("texte"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Livrable"


# ── Page Services (index unique) ───────────────────────────────────────────────
class ServicesIndexPage(Page):
    """
    Page /services/ — liste tous les services d'Innov Geomatics.
    Un seul instance, enfant de HomePage.
    """

    intro = models.TextField(
        verbose_name="Introduction",
        blank=True,
        default=(
            "De l'analyse spatiale à la cartographie web, Innov Geomatics vous accompagne "
            "à chaque étape de vos projets géomatiques avec des technologies open source "
            "et une expertise terrain."
        ),
    )

    # ── SEO
    seo_description = models.TextField(
        blank=True,
        verbose_name="Description SEO",
        default="SIG, télédétection, cartographie web et conseil géospatial par Innov Geomatics Consulting à Ouagadougou.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("seo_description"),
        MultiFieldPanel(
            [InlinePanel("livrables", label="Livrable")],
            heading="Livrables par service (optionnel — remplace les défauts)",
        ),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["services"] = _get_services_data()
        context["process_steps"] = _get_process_steps()
        return context

    class Meta:
        verbose_name = "Page Services"


# ── Données statiques (à migrer vers Snippet si tu veux les éditer en admin) ──

def _get_services_data():
    return [
        {
            "id":          "gis",
            "emoji":       "🗺️",
            "bg_class":    "bg-sky/10",
            "title":       "Systèmes d'Information Géographique",
            "description": (
                "Conception et mise en œuvre de bases de données spatiales adaptées à vos besoins : "
                "inventaires fonciers, suivi de l'occupation du sol, gestion d'infrastructures. "
                "Nous produisons des cartes thématiques de haute qualité et réalisons des analyses spatiales poussées."
            ),
            "tags":        ["QGIS", "PostGIS", "PostgreSQL", "Cartographie thématique", "Analyse spatiale"],
            "livrables": [
                "Bases de données spatiales (PostGIS)",
                "Cartes thématiques haute résolution",
                "Rapports d'analyse spatiale",
                "Atlas cartographiques PDF",
                "Formation à la prise en main",
            ],
        },
        {
            "id":          "teledetection",
            "emoji":       "🛰️",
            "bg_class":    "bg-navy/10",
            "title":       "Télédétection & Analyse d'images",
            "description": (
                "Exploitation d'images satellites (Sentinel, Landsat, Spot) et de données drones "
                "pour le suivi environnemental, agricole et urbain. Classification supervisée, "
                "calcul d'indices (NDVI, NDWI, NBR) et détection de changements."
            ),
            "tags":        ["Sentinel-2", "SNAP", "Python", "NDVI / NDWI", "Drones"],
            "livrables": [
                "Cartes d'occupation du sol",
                "Indices de végétation et eau",
                "Rapports de suivi temporel",
                "Orthophotos traitées",
                "Scripts Python réutilisables",
            ],
        },
        {
            "id":          "webmapping",
            "emoji":       "🌐",
            "bg_class":    "bg-sky/10",
            "title":       "Cartographie Web & Applications SIG",
            "description": (
                "Développement d'applications cartographiques interactives accessibles depuis un navigateur. "
                "Visualisation de données géospatiales en temps réel, tableaux de bord thématiques, "
                "collecte de données terrain avec synchronisation offline."
            ),
            "tags":        ["Leaflet.js", "Django", "PostGIS", "GeoServer", "Flutter"],
            "livrables": [
                "Application web cartographique",
                "API REST géospatiale",
                "Application mobile de collecte terrain",
                "Dashboard de suivi",
                "Documentation technique",
            ],
        },
        {
            "id":          "conseil",
            "emoji":       "🤝",
            "bg_class":    "bg-navy/10",
            "title":       "Conseil & Expertise",
            "description": (
                "Accompagnement stratégique pour la mise en place de SIG en entreprise ou institution publique. "
                "Audit de données existantes, recommandations d'outils et de workflows, "
                "rédaction de cahiers des charges techniques."
            ),
            "tags":        ["Audit SIG", "Stratégie géospatiale", "Cahier des charges", "Transfert de compétences"],
            "livrables": [
                "Rapport d'audit géospatial",
                "Cahier des charges technique",
                "Plan de mise en œuvre",
                "Recommandations d'outils",
            ],
        },
    ]


def _get_process_steps():
    return [
        {
            "num":         "01",
            "title":       "Cadrage",
            "description": "Analyse des besoins, définition des objectifs et du périmètre du projet.",
            "accent":      False,
        },
        {
            "num":         "02",
            "title":       "Collecte",
            "description": "Acquisition des données terrain, satellitaires ou existantes.",
            "accent":      True,
        },
        {
            "num":         "03",
            "title":       "Traitement",
            "description": "Analyse, modélisation et production des livrables géospatiaux.",
            "accent":      False,
        },
        {
            "num":         "04",
            "title":       "Livraison",
            "description": "Transfert des livrables, formation et suivi post-projet.",
            "accent":      True,
        },
    ]
