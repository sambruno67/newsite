from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
        ("wagtailimages", "0026_delete_uploadedimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Formation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titre", models.CharField(max_length=255, verbose_name="Titre")),
                ("slug", models.SlugField(blank=True, unique=True, verbose_name="Slug URL")),
                ("description_courte", models.TextField(verbose_name="Description courte")),
                ("description", wagtail.fields.RichTextField(blank=True, verbose_name="Description complète")),
                ("est_disponible", models.BooleanField(default=False, verbose_name="Disponible à l'inscription")),
                ("categorie", models.CharField(choices=[("gis","SIG & QGIS"),("teledetection","Télédétection"),("webmapping","Cartographie Web"),("collecte","Collecte de données"),("autre","Autre")], default="gis", max_length=20, verbose_name="Catégorie")),
                ("modalite", models.CharField(choices=[("presentiel","Présentiel"),("enligne","En ligne"),("hybride","Hybride")], default="presentiel", max_length=12, verbose_name="Modalité")),
                ("duree", models.CharField(blank=True, max_length=60, verbose_name="Durée")),
                ("nb_participants", models.CharField(blank=True, max_length=60, verbose_name="Participants")),
                ("lieu", models.CharField(blank=True, max_length=120, verbose_name="Lieu")),
                ("prix", models.PositiveIntegerField(blank=True, null=True, verbose_name="Prix (FCFA)")),
                ("ordre", models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("image", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="wagtailimages.image", verbose_name="Image de couverture")),
            ],
            options={"verbose_name": "Formation", "verbose_name_plural": "Formations", "ordering": ["ordre", "titre"]},
        ),
        migrations.CreateModel(
            name="ModuleFormation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                ("titre", models.CharField(max_length=255, verbose_name="Intitulé du module")),
                ("formation", modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name="modules", to="formations.formation")),
            ],
            options={"verbose_name": "Module", "ordering": ["sort_order"], "abstract": False},
        ),
        migrations.CreateModel(
            name="FormationsIndexPage",
            fields=[
                ("page_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("intro", models.TextField(blank=True, verbose_name="Introduction")),
                ("stat_formes", models.PositiveIntegerField(default=200, verbose_name="Professionnels formés")),
                ("stat_programmes", models.PositiveIntegerField(default=8, verbose_name="Nombre de programmes")),
                ("stat_satisfaction", models.PositiveIntegerField(default=95, verbose_name="Taux de satisfaction (%)")),
                ("lms_url", models.URLField(blank=True, default="https://learn.innovgeomatic.com", verbose_name="URL plateforme LMS")),
            ],
            options={"verbose_name": "Page Formations"},
            bases=("wagtailcore.page",),
        ),
    ]
