from django.contrib import admin
from .models import Contact, Echange, Relance, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["nom", "couleur"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display  = ["nom_complet", "organisation", "email", "statut", "pipeline", "created_at"]
    list_filter   = ["statut", "pipeline", "source", "tags"]
    search_fields = ["nom", "prenom", "email", "organisation"]
    filter_horizontal = ["tags"]

@admin.register(Echange)
class EchangeAdmin(admin.ModelAdmin):
    list_display = ["contact", "type_echange", "titre", "date"]
    list_filter  = ["type_echange"]

@admin.register(Relance)
class RelanceAdmin(admin.ModelAdmin):
    list_display = ["contact", "titre", "date_prevue", "priorite", "effectuee"]
    list_filter  = ["priorite", "effectuee"]
