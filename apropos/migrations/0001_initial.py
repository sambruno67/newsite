from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="AProposPage",
            fields=[
                ("page_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
                ("intro", models.TextField(blank=True, verbose_name="Introduction")),
                ("mission", models.TextField(verbose_name="Mission")),
                ("vision", models.TextField(verbose_name="Vision")),
                ("valeurs", wagtail.fields.RichTextField(blank=True, verbose_name="Valeurs")),
            ],
            options={"verbose_name": "Page À propos"},
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="MembreEquipe",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                ("initiales", models.CharField(max_length=3, verbose_name="Initiales")),
                ("nom", models.CharField(max_length=100, verbose_name="Nom complet")),
                ("poste", models.CharField(max_length=150, verbose_name="Poste / rôle")),
                ("competences", models.CharField(blank=True, max_length=300, verbose_name="Compétences")),
                ("couleur_bg", models.CharField(blank=True, default="linear-gradient(135deg,#1A3A8F,#29ABE2)", max_length=100, verbose_name="Couleur de fond avatar")),
                ("page", modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name="membres", to="apropos.apropospage")),
            ],
            options={"ordering": ["sort_order"], "abstract": False},
        ),
        migrations.CreateModel(
            name="EtapeTimeline",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                ("annee", models.CharField(max_length=10, verbose_name="Année")),
                ("titre", models.CharField(max_length=200, verbose_name="Titre")),
                ("description", models.TextField(verbose_name="Description")),
                ("est_actuel", models.BooleanField(default=False, verbose_name="Étape actuelle")),
                ("page", modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name="timeline", to="apropos.apropospage")),
            ],
            options={"ordering": ["sort_order"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Partenaire",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("sort_order", models.IntegerField(blank=True, editable=False, null=True)),
                ("emoji", models.CharField(blank=True, default="🏢", max_length=4, verbose_name="Emoji")),
                ("nom", models.CharField(max_length=150, verbose_name="Nom du partenaire")),
                ("page", modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name="partenaires", to="apropos.apropospage")),
            ],
            options={"ordering": ["sort_order"], "abstract": False},
        ),
    ]
