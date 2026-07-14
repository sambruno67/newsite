from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sujet", models.CharField(choices=[("devis","Demande de devis"),("formation","Formation"),("partenariat","Partenariat"),("renseignement","Renseignement"),("autre","Autre")], default="devis", max_length=20, verbose_name="Sujet")),
                ("prenom", models.CharField(max_length=100, verbose_name="Prénom")),
                ("nom", models.CharField(max_length=100, verbose_name="Nom")),
                ("email", models.EmailField(verbose_name="Email")),
                ("telephone", models.CharField(blank=True, max_length=30, verbose_name="Téléphone")),
                ("organisation", models.CharField(blank=True, max_length=200, verbose_name="Organisation")),
                ("message", models.TextField(verbose_name="Message")),
                ("formation_ref", models.CharField(blank=True, max_length=100, verbose_name="Formation concernée (slug)")),
                ("service_ref", models.CharField(blank=True, max_length=100, verbose_name="Service concerné")),
                ("lu", models.BooleanField(default=False, verbose_name="Lu")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Reçu le")),
            ],
            options={"verbose_name": "Message reçu", "verbose_name_plural": "Messages reçus", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ContactPage",
            fields=[
                ("page_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("intro", models.TextField(blank=True, verbose_name="Introduction")),
                ("adresse", models.CharField(blank=True, default="Ouagadougou, Burkina Faso", max_length=255, verbose_name="Adresse")),
                ("email_public", models.EmailField(blank=True, default="contact@innovgeomatic.com", verbose_name="Email public")),
                ("telephone", models.CharField(blank=True, max_length=30, verbose_name="Téléphone")),
                ("horaires", models.TextField(blank=True, verbose_name="Horaires")),
                ("email_destinataire", models.EmailField(blank=True, default="contact@innovgeomatic.com", verbose_name="Email destinataire des messages")),
                ("linkedin", models.URLField(blank=True, verbose_name="LinkedIn URL")),
                ("twitter", models.URLField(blank=True, verbose_name="Twitter/X URL")),
                ("facebook", models.URLField(blank=True, verbose_name="Facebook URL")),
            ],
            options={"verbose_name": "Page Contact"},
            bases=("wagtailcore.page",),
        ),
    ]
