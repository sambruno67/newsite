from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nom", models.CharField(max_length=50, unique=True, verbose_name="Nom")),
                ("couleur", models.CharField(choices=[("blue","Bleu — SIG"),("green","Vert — Formation"),("purple","Violet — Web"),("amber","Ambre — Télédétection"),("gray","Gris — Autre")], default="blue", max_length=20, verbose_name="Couleur")),
            ],
            options={"verbose_name": "Tag", "verbose_name_plural": "Tags", "ordering": ["nom"]},
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("prenom", models.CharField(blank=True, max_length=100, verbose_name="Prénom")),
                ("nom", models.CharField(max_length=100, verbose_name="Nom / Organisation")),
                ("email", models.EmailField(blank=True, verbose_name="Email")),
                ("telephone", models.CharField(blank=True, max_length=30, verbose_name="Téléphone")),
                ("organisation", models.CharField(blank=True, max_length=200, verbose_name="Organisation")),
                ("lieu", models.CharField(blank=True, max_length=200, verbose_name="Lieu / Pays")),
                ("poste", models.CharField(blank=True, max_length=150, verbose_name="Poste / Fonction")),
                ("statut", models.CharField(choices=[("nouveau","Nouveau"),("prospect","Prospect"),("en_cours","En cours"),("client","Client"),("archive","Archivé")], default="nouveau", max_length=20, verbose_name="Statut")),
                ("pipeline", models.CharField(choices=[("nouveau","Nouveau"),("contacte","Contacté"),("devis","Devis envoyé"),("negociation","Négociation"),("gagne","Gagné"),("perdu","Perdu")], default="nouveau", max_length=20, verbose_name="Étape pipeline")),
                ("valeur_devis", models.PositiveIntegerField(blank=True, null=True, verbose_name="Valeur devis (FCFA)")),
                ("date_devis", models.DateField(blank=True, null=True, verbose_name="Date devis")),
                ("source", models.CharField(choices=[("site","Formulaire site"),("telephone","Téléphone"),("email","Email direct"),("reseau","Réseau / recommandation"),("evenement","Événement"),("autre","Autre")], default="site", max_length=20, verbose_name="Source")),
                ("notes", models.TextField(blank=True, verbose_name="Notes internes")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Créé le")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Modifié le")),
                ("tags", models.ManyToManyField(blank=True, to="crm.tag", verbose_name="Tags")),
                ("responsable", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="contacts", to="auth.user", verbose_name="Responsable")),
            ],
            options={"verbose_name": "Contact", "verbose_name_plural": "Contacts", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Echange",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type_echange", models.CharField(choices=[("message","Message reçu"),("email","Email envoyé"),("appel","Appel téléphonique"),("reunion","Réunion"),("devis","Devis envoyé"),("contrat","Contrat signé"),("livraison","Livraison"),("note","Note interne")], default="note", max_length=20, verbose_name="Type")),
                ("titre", models.CharField(max_length=200, verbose_name="Titre / Résumé")),
                ("contenu", models.TextField(blank=True, verbose_name="Détails")),
                ("date", models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date")),
                ("contact", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="echanges", to="crm.contact")),
                ("auteur", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="echanges", to="auth.user", verbose_name="Auteur")),
            ],
            options={"verbose_name": "Échange", "verbose_name_plural": "Échanges", "ordering": ["-date"]},
        ),
        migrations.CreateModel(
            name="Relance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titre", models.CharField(max_length=200, verbose_name="Objet de la relance")),
                ("date_prevue", models.DateField(verbose_name="Date prévue")),
                ("priorite", models.CharField(choices=[("basse","Basse"),("normale","Normale"),("haute","Haute"),("urgente","Urgente")], default="normale", max_length=10, verbose_name="Priorité")),
                ("effectuee", models.BooleanField(default=False, verbose_name="Effectuée")),
                ("notes", models.TextField(blank=True, verbose_name="Notes")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("contact", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="relances", to="crm.contact")),
            ],
            options={"verbose_name": "Relance", "verbose_name_plural": "Relances", "ordering": ["effectuee", "date_prevue"]},
        ),
    ]
