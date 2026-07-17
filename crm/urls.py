from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    path("crm/",                          views.dashboard,       name="dashboard"),
    path("crm/pipeline/",                 views.pipeline,        name="pipeline"),
    path("crm/contacts/",                 views.liste_contacts,  name="liste_contacts"),
    path("crm/contacts/nouveau/",         views.creer_contact,   name="creer_contact"),
    path("crm/contacts/<int:pk>/",        views.fiche_contact,   name="fiche_contact"),
    path("crm/relances/",                 views.liste_relances,  name="liste_relances"),
    path("crm/importer/<int:message_id>/", views.importer_message, name="importer_message"),
    path("crm/export/",  views.export_contacts_csv, name="export_csv"),
    path("crm/import/",  views.import_contacts_csv, name="import_csv"),
]
