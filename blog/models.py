from django.db import models
from django.utils.text import slugify
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


# ══════════════════════════════════════════════════════════════════════
# Tag
# ══════════════════════════════════════════════════════════════════════

class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPost",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


# ══════════════════════════════════════════════════════════════════════
# Article de blog (Page Wagtail)
# ══════════════════════════════════════════════════════════════════════

class BlogPost(Page):

    CATEGORIE_CHOICES = [
        ("sig",        "SIG & QGIS"),
        ("teledetection", "Télédétection"),
        ("webmapping", "Cartographie Web"),
        ("python",     "Python & QGIS"),
        ("actualite",  "Actualités"),
        ("autre",      "Autre"),
    ]

    # ── Contenu ───────────────────────────────────────────────────────
    chapeau = models.TextField(
        verbose_name="Chapeau (introduction)",
        blank=True,
        help_text="Résumé affiché sur les cards et en intro de l'article.",
    )
    corps = RichTextField(verbose_name="Corps de l'article")

    # ── Méta ──────────────────────────────────────────────────────────
    categorie    = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default="sig", verbose_name="Catégorie")
    auteur       = models.CharField(max_length=100, blank=True, default="Innov Geomatics", verbose_name="Auteur")
    date_publi   = models.DateField(verbose_name="Date de publication")
    temps_lecture = models.PositiveIntegerField(default=5, verbose_name="Temps de lecture (min)")
    est_phare    = models.BooleanField(default=False, verbose_name="Article phare", help_text="Affiché en grand en haut du blog.")

    # ── Image ─────────────────────────────────────────────────────────
    image_principale = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )
    emoji_fallback = models.CharField(max_length=4, blank=True, default="📰", verbose_name="Emoji (si pas d'image)")

    # ── Tags ──────────────────────────────────────────────────────────
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    # ── Recherche ─────────────────────────────────────────────────────
    search_fields = Page.search_fields + [
        index.SearchField("chapeau"),
        index.SearchField("corps"),
        index.FilterField("categorie"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("chapeau"),
            FieldPanel("corps"),
        ], heading="Contenu"),
        MultiFieldPanel([
            FieldPanel("categorie"),
            FieldPanel("auteur"),
            FieldPanel("date_publi"),
            FieldPanel("temps_lecture"),
            FieldPanel("est_phare"),
            FieldPanel("tags"),
        ], heading="Méta"),
        FieldPanel("image_principale"),
        FieldPanel("emoji_fallback"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types     = []

    class Meta:
        verbose_name        = "Article de blog"
        verbose_name_plural = "Articles de blog"

    def __str__(self):
        return self.title

    @property
    def initiales_auteur(self):
        parts = self.auteur.split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        return self.auteur[:2].upper()


# ══════════════════════════════════════════════════════════════════════
# Page index Blog
# ══════════════════════════════════════════════════════════════════════

class BlogIndexPage(Page):
    """Page /blog/ — liste tous les articles."""

    intro = models.TextField(
        blank=True,
        verbose_name="Introduction",
        default="Tutoriels, actualités SIG, télédétection et cartographie web — par l'équipe Innov Geomatics.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types     = ["blog.BlogPost"]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        categorie = request.GET.get("cat", "")
        tag       = request.GET.get("tag", "")
        page_num  = int(request.GET.get("page", 1))

        # Tous les articles publiés, triés par date
        posts = BlogPost.objects.live().order_by("-date_publi")

        if categorie:
            posts = posts.filter(categorie=categorie)
        if tag:
            posts = posts.filter(tags__slug=tag)

        # Article phare
        context["article_phare"]    = posts.filter(est_phare=True).first()
        context["articles"]         = posts.filter(est_phare=False)[:8]
        context["categorie_active"] = categorie
        context["tag_actif"]        = tag
        context["categories"]       = BlogPost.CATEGORIE_CHOICES

        # Comptage par catégorie
        from django.db.models import Count
        context["cat_counts"] = {
            cat: BlogPost.objects.live().filter(categorie=cat).count()
            for cat, _ in BlogPost.CATEGORIE_CHOICES
        }

        # Articles populaires (les 3 plus récents phares ou bien lus)
        context["articles_populaires"] = BlogPost.objects.live().order_by("-date_publi")[:3]

        return context

    class Meta:
        verbose_name = "Page Blog"
