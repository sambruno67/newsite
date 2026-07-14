import os
from django.core.wsgi import get_wsgi_application

# Lit la variable d'environnement directement, sans setdefault
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    os.environ["DJANGO_SETTINGS_MODULE"] = "innovgeomatic.settings.dev"

application = get_wsgi_application()