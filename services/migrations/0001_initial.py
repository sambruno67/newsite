from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServicesIndexPage",
            fields=[
                ("page_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("intro", models.TextField(blank=True, default="De l'analyse spatiale à la cartographie web, Innov Geomatics vous accompagne à chaque étape de vos projets géomatiques avec des technologies open source et une expertise terrain.", verbose_name="Introduction")),
                ("seo_description", models.TextField(blank=True, default="SIG, télédétection, cartographie web et conseil géospatial par Innov Geomatics Consulting à Ouagadougou.", verbose_name="Description SEO")),
            ],
            options={
                "verbose_name": "Page Services",
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="ServiceLivrable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                ("service", models.CharField(choices=[("gis", "SIG & Cartographie"), ("teledetection", "Télédétection"), ("webmapping", "Cartographie Web"), ("conseil", "Conseil & Expertise")], max_length=20, verbose_name="Service concerné")),
                ("texte", models.CharField(max_length=200, verbose_name="Livrable")),
                ("page", modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name="livrables", to="services.servicesindexpage")),
            ],
            options={
                "verbose_name": "Livrable",
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]
