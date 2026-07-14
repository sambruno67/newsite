from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
        ("wagtailimages", "0026_delete_uploadedimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Projet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titre", models.CharField(max_length=255, verbose_name="Titre")),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("description_courte", models.TextField(verbose_name="Description courte")),
                ("description", wagtail.fields.RichTextField(blank=True, verbose_name="Description complète")),
                ("client", models.CharField(blank=True, max_length=200, verbose_name="Client / Commanditaire")),
                ("lieu", models.CharField(blank=True, max_length=200, verbose_name="Lieu / Pays")),
                ("categorie", models.CharField(choices=[("gis","SIG & Cartographie"),("teledetection","Télédétection"),("webmapping","Cartographie Web"),("foncier","Foncier"),("agriculture","Agriculture"),("environnement","Environnement"),("autre","Autre")], default="gis", max_length=20, verbose_name="Catégorie")),
                ("est_phare", models.BooleanField(default=False, verbose_name="Projet phare")),
                ("date", models.DateField(verbose_name="Date de livraison")),
                ("ordre", models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ("emoji_fallback", models.CharField(blank=True, default="🗺️", max_length=4, verbose_name="Emoji (si pas d'image)")),
                ("technologies", models.CharField(blank=True, max_length=500, verbose_name="Technologies")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("image", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="wagtailimages.image", verbose_name="Image principale")),
            ],
            options={"verbose_name": "Projet", "verbose_name_plural": "Projets", "ordering": ["-date", "ordre"]},
        ),
        migrations.CreateModel(
            name="ProjetsIndexPage",
            fields=[
                ("page_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("intro", models.TextField(blank=True, verbose_name="Introduction")),
                ("stat_projets", models.PositiveIntegerField(default=50, verbose_name="Projets livrés")),
                ("stat_pays", models.PositiveIntegerField(default=12, verbose_name="Pays couverts")),
                ("stat_clients", models.PositiveIntegerField(default=30, verbose_name="Clients satisfaits")),
                ("stat_experience", models.PositiveIntegerField(default=8, verbose_name="Années d'expérience")),
            ],
            options={"verbose_name": "Page Projets"},
            bases=("wagtailcore.page",),
        ),
    ]
