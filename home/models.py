from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):

    hero_subtitle = models.TextField(
        verbose_name="Sous-titre héro",
        blank=True,
        default="Innov Geomatics Consulting accompagne les organisations dans leurs projets SIG, télédétection et cartographie web — de Ouagadougou à l'ensemble du continent."
    )
    stat_projects  = models.PositiveIntegerField(default=50)
    stat_trained   = models.PositiveIntegerField(default=200)
    stat_countries = models.PositiveIntegerField(default=10)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_subtitle"),
        ], heading="Héro"),
        MultiFieldPanel([
            FieldPanel("stat_projects"),
            FieldPanel("stat_trained"),
            FieldPanel("stat_countries"),
        ], heading="Statistiques"),
    ]

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "services.ServicesIndexPage",
        "formations.FormationsIndexPage",
        "contact.ContactPage",
        "projets.ProjetsIndexPage",
        "blog.BlogIndexPage",
        ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        try:
            from formations.models import Formation
            context["formations"] = Formation.objects.filter(
                est_disponible=True
            ).order_by("ordre")[:6]
        except Exception:
            context["formations"] = []
        return context

    class Meta:
        verbose_name = "Page d'accueil"