from django.apps import AppConfig

class FormationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "formations"           # ← doit correspondre au nom du dossier
    verbose_name = "Formations"
