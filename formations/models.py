from django.db import models
from django.utils.text import slugify
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


# ══════════════════════════════════════════════════════════════════════
# Module de formation
# ══════════════════════════════════════════════════════════════════════

class ModuleFormation(ClusterableModel, Orderable):
    formation = ParentalKey(
        "Formation",
        on_delete=models.CASCADE,
        related_name="modules",
    )
    titre       = models.CharField(max_length=255, verbose_name="Titre du module")
    description = models.TextField(blank=True, verbose_name="Description du module")

    panels = [
        FieldPanel("titre"),
        FieldPanel("description"),
        InlinePanel("lecons", label="Leçon"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Module"

    def __str__(self):
        return self.titre


# ══════════════════════════════════════════════════════════════════════
# Leçon d'un module
# ══════════════════════════════════════════════════════════════════════

class LeconModule(Orderable):
    module = ParentalKey(
        "ModuleFormation",
        on_delete=models.CASCADE,
        related_name="lecons",
    )
    titre    = models.CharField(max_length=255, verbose_name="Titre de la leçon")
    est_projet = models.BooleanField(default=False, verbose_name="Projet / évaluation finale")

    panels = [
        FieldPanel("titre"),
        FieldPanel("est_projet"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Leçon"

    def __str__(self):
        return self.titre


# ══════════════════════════════════════════════════════════════════════
# Formateur
# ══════════════════════════════════════════════════════════════════════

class FormateurFormation(Orderable):
    formation   = ParentalKey(
        "Formation",
        on_delete=models.CASCADE,
        related_name="formateurs",
    )
    initiales   = models.CharField(max_length=3, verbose_name="Initiales")
    nom         = models.CharField(max_length=100, verbose_name="Nom complet")
    role        = models.CharField(max_length=200, verbose_name="Rôle / poste")
    competences = models.CharField(
        max_length=300, blank=True,
        verbose_name="Compétences (séparées par virgules)",
    )

    panels = [
        FieldPanel("initiales"),
        FieldPanel("nom"),
        FieldPanel("role"),
        FieldPanel("competences"),
    ]

    @property
    def competences_list(self):
        return [c.strip() for c in self.competences.split(",") if c.strip()]


# ══════════════════════════════════════════════════════════════════════
# Document téléchargeable
# ══════════════════════════════════════════════════════════════════════

class DocumentFormation(Orderable):
    formation = ParentalKey(
        "Formation",
        on_delete=models.CASCADE,
        related_name="documents",
    )
    titre    = models.CharField(max_length=200, verbose_name="Titre du document")
    fichier  = models.ForeignKey(
        "wagtaildocs.Document",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Fichier",
    )
    taille   = models.CharField(max_length=20, blank=True, verbose_name="Taille (ex: 245 Ko)")

    panels = [
        FieldPanel("titre"),
        FieldPanel("fichier"),
        FieldPanel("taille"),
    ]


# ══════════════════════════════════════════════════════════════════════
# Prérequis
# ══════════════════════════════════════════════════════════════════════

class PrerequisFormation(Orderable):
    formation = ParentalKey(
        "Formation",
        on_delete=models.CASCADE,
        related_name="prerequis",
    )
    texte    = models.CharField(max_length=200, verbose_name="Prérequis")
    requis   = models.BooleanField(default=True, verbose_name="Requis (coché) / Non requis (décoché)")

    panels = [
        FieldPanel("texte"),
        FieldPanel("requis"),
    ]


# ══════════════════════════════════════════════════════════════════════
# Formation principale
# ══════════════════════════════════════════════════════════════════════

@register_snippet
class Formation(ClusterableModel):

    CATEGORIE_CHOICES = [
        ("gis",           "SIG & QGIS"),
        ("teledetection", "Télédétection"),
        ("webmapping",    "Cartographie Web"),
        ("collecte",      "Collecte de données"),
        ("python",        "Python & Géomatique"),
        ("autre",         "Autre"),
    ]

    MODALITE_CHOICES = [
        ("presentiel", "Présentiel"),
        ("enligne",    "En ligne"),
        ("hybride",    "Hybride"),
    ]

    NIVEAU_CHOICES = [
        ("debutant",      "Débutant"),
        ("intermediaire", "Intermédiaire"),
        ("avance",        "Avancé"),
        ("tous",          "Tous niveaux"),
    ]

    # ── Infos principales ─────────────────────────────────────────────
    titre              = models.CharField(max_length=255, verbose_name="Titre")
    slug               = models.SlugField(unique=True, blank=True, verbose_name="Slug URL")
    description_courte = models.TextField(verbose_name="Description courte")
    description        = RichTextField(verbose_name="Description complète", blank=True)

    # ── Statut ────────────────────────────────────────────────────────
    est_disponible = models.BooleanField(default=False, verbose_name="Disponible à l'inscription")
    categorie      = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default="gis")
    modalite       = models.CharField(max_length=12, choices=MODALITE_CHOICES, default="presentiel")
    niveau         = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default="debutant")

    # ── Détails pratiques ─────────────────────────────────────────────
    duree              = models.CharField(max_length=60,  blank=True, verbose_name="Durée (ex : 5 jours / 40h)")
    nb_participants    = models.CharField(max_length=60,  blank=True, verbose_name="Participants (ex : 8–15 pers.)")
    lieu               = models.CharField(max_length=120, blank=True, verbose_name="Lieu")
    langue             = models.CharField(max_length=60,  blank=True, default="Français", verbose_name="Langue")
    materiel           = models.CharField(max_length=120, blank=True, verbose_name="Matériel fourni")
    prochaine_session  = models.CharField(max_length=100, blank=True, verbose_name="Prochaine session (ex : Août 2025)")
    prix               = models.PositiveIntegerField(null=True, blank=True, verbose_name="Prix (FCFA)")
    prix_description   = models.CharField(
        max_length=200, blank=True,
        default="Par participant · Déjeuners inclus · Support de cours PDF",
        verbose_name="Description du prix",
    )

    # ── TDR ───────────────────────────────────────────────────────────
    tdr_contexte       = models.TextField(blank=True, verbose_name="Contexte et justification")
    tdr_objectifs      = models.TextField(blank=True, verbose_name="Objectifs généraux (un par ligne)")
    tdr_public         = models.TextField(blank=True, verbose_name="Public cible (un par ligne)")
    tdr_resultats      = models.TextField(blank=True, verbose_name="Résultats attendus (un par ligne)")
    tdr_methodologie   = models.TextField(blank=True, verbose_name="Méthodologie")

    # ── Certification ─────────────────────────────────────────────────
    avec_certificat    = models.BooleanField(default=True, verbose_name="Certificat inclus")
    certificat_description = models.TextField(
        blank=True,
        default="Délivré après validation du projet final. Téléchargeable en PDF avec QR code de vérification.",
        verbose_name="Description du certificat",
    )

    # ── Ordre & image ─────────────────────────────────────────────────
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de couverture",
    )
    emoji_fallback = models.CharField(max_length=4, blank=True, default="🎓", verbose_name="Emoji fallback")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ── Admin panels ──────────────────────────────────────────────────
    panels = [
        MultiFieldPanel([
            FieldPanel("titre"),
            FieldPanel("slug"),
            FieldPanel("description_courte"),
            FieldPanel("description"),
            FieldPanel("image"),
            FieldPanel("emoji_fallback"),
        ], heading="Contenu principal"),

        MultiFieldPanel([
            FieldPanel("est_disponible"),
            FieldPanel("categorie"),
            FieldPanel("modalite"),
            FieldPanel("niveau"),
            FieldPanel("ordre"),
        ], heading="Statut & catégorie"),

        MultiFieldPanel([
            FieldPanel("duree"),
            FieldPanel("nb_participants"),
            FieldPanel("lieu"),
            FieldPanel("langue"),
            FieldPanel("materiel"),
            FieldPanel("prochaine_session"),
            FieldPanel("prix"),
            FieldPanel("prix_description"),
        ], heading="Infos pratiques"),

        MultiFieldPanel([
            FieldPanel("tdr_contexte"),
            FieldPanel("tdr_objectifs"),
            FieldPanel("tdr_public"),
            FieldPanel("tdr_resultats"),
            FieldPanel("tdr_methodologie"),
        ], heading="TDR — Termes de référence"),

        MultiFieldPanel([
            FieldPanel("avec_certificat"),
            FieldPanel("certificat_description"),
        ], heading="Certification"),

        InlinePanel("modules",    label="Module du programme"),
        InlinePanel("formateurs", label="Formateur"),
        InlinePanel("prerequis",  label="Prérequis"),
        InlinePanel("documents",  label="Document téléchargeable"),
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

    @property
    def tdr_objectifs_list(self):
        return [l.strip() for l in self.tdr_objectifs.splitlines() if l.strip()]

    @property
    def tdr_public_list(self):
        return [l.strip() for l in self.tdr_public.splitlines() if l.strip()]

    @property
    def tdr_resultats_list(self):
        return [l.strip() for l in self.tdr_resultats.splitlines() if l.strip()]


# ══════════════════════════════════════════════════════════════════════
# Pages Wagtail
# ══════════════════════════════════════════════════════════════════════

class FormationsIndexPage(Page):
    intro = models.TextField(blank=True, default="Des formations pratiques animés par des experts terrain.")
    stat_formes       = models.PositiveIntegerField(default=200)
    stat_programmes   = models.PositiveIntegerField(default=8)
    stat_satisfaction = models.PositiveIntegerField(default=95)
    lms_url           = models.URLField(blank=True, default="https://learn.innovgeomatic.com")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel([
            FieldPanel("stat_formes"),
            FieldPanel("stat_programmes"),
            FieldPanel("stat_satisfaction"),
        ], heading="Statistiques"),
        FieldPanel("lms_url"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        categorie = request.GET.get("cat", "")
        modalite  = request.GET.get("mode", "")
        qs = Formation.objects.all()
        if categorie:
            qs = qs.filter(categorie=categorie)
        if modalite:
            qs = qs.filter(modalite=modalite)
        context["formations_dispo"]  = qs.filter(est_disponible=True).order_by("ordre")
        context["formations_coming"] = qs.filter(est_disponible=False).order_by("ordre")
        context["categorie_active"]  = categorie
        context["modalite_active"]   = modalite
        context["categories"]        = Formation.CATEGORIE_CHOICES
        context["modalites"]         = Formation.MODALITE_CHOICES
        return context

    class Meta:
        verbose_name = "Page Formations"
