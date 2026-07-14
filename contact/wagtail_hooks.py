from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.panels import FieldPanel

from .models import ContactMessage


class ContactMessageAdmin(SnippetViewSet):
    model        = ContactMessage
    menu_label   = "Messages reçus"
    menu_icon    = "mail"
    list_display = ["__str__", "email", "sujet", "lu", "created_at"]
    list_filter  = ["sujet", "lu"]
    search_fields = ["prenom", "nom", "email", "message"]
    panels = [
        FieldPanel("sujet"),
        FieldPanel("prenom"),
        FieldPanel("nom"),
        FieldPanel("email"),
        FieldPanel("telephone"),
        FieldPanel("organisation"),
        FieldPanel("message"),
        FieldPanel("lu"),
    ]


register_snippet(ContactMessageAdmin)
