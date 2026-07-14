from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.fields
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("taggit", "0001_initial"),
        ("wagtailcore", "0094_alter_page_locale"),
        ("wagtailimages", "0026_delete_uploadedimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogIndexPage",
            fields=[
                ("page_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("intro", models.TextField(blank=True, verbose_name="Introduction")),
            ],
            options={"verbose_name": "Page Blog"},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("page_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("chapeau", models.TextField(blank=True, verbose_name="Chapeau (introduction)")),
                ("corps", wagtail.fields.RichTextField(verbose_name="Corps de l'article")),
                ("categorie", models.CharField(choices=[("sig","SIG & QGIS"),("teledetection","Télédétection"),("webmapping","Cartographie Web"),("python","Python & QGIS"),("actualite","Actualités"),("autre","Autre")], default="sig", max_length=20, verbose_name="Catégorie")),
                ("auteur", models.CharField(blank=True, default="Innov Geomatics", max_length=100, verbose_name="Auteur")),
                ("date_publi", models.DateField(verbose_name="Date de publication")),
                ("temps_lecture", models.PositiveIntegerField(default=5, verbose_name="Temps de lecture (min)")),
                ("est_phare", models.BooleanField(default=False, verbose_name="Article phare")),
                ("emoji_fallback", models.CharField(blank=True, default="📰", max_length=4, verbose_name="Emoji (si pas d'image)")),
                ("image_principale", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="wagtailimages.image", verbose_name="Image principale")),
            ],
            options={"verbose_name": "Article de blog", "verbose_name_plural": "Articles de blog"},
            bases=("wagtailcore.page", wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name="BlogPostTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content_object", modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name="tagged_items", to="blog.blogpost")),
                ("tag", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="%(app_label)s_%(class)s_items", to="taggit.tag")),
            ],
            options={"abstract": False},
        ),
    ]
