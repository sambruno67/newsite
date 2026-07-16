from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ══════════════════════════════════════════════════════════════════════
# Tags
# ══════════════════════════════════════════════════════════════════════

class Tag(models.Model):
    nom    = models.CharField(max_length=50, unique=True, verbose_name="Nom")
    couleur = models.CharField(
        max_length=20,
        default="blue",
        choices=[
            ("blue",   "Bleu — SIG"),
            ("green",  "Vert — Formation"),
            ("purple", "Violet — Web"),
            ("amber",  "Ambre — Télédétection"),
            ("gray",   "Gris — Autre"),
        ],
        verbose_name="Couleur",
    )

    class Meta:
        verbose_name        = "Tag"
        verbose_name_plural = "Tags"
        ordering            = ["nom"]

    def __str__(self):
        return self.nom


# ══════════════════════════════════════════════════════════════════════
# Contact / Client
# ══════════════════════════════════════════════════════════════════════

class Contact(models.Model):

    STATUT_CHOICES = [
        ("nouveau",      "Nouveau"),
        ("prospect",     "Prospect"),
        ("en_cours",     "En cours"),
        ("client",       "Client"),
        ("archive",      "Archivé"),
    ]

    PIPELINE_CHOICES = [
        ("nouveau",      "Nouveau"),
        ("contacte",     "Contacté"),
        ("devis",        "Devis envoyé"),
        ("negociation",  "Négociation"),
        ("gagne",        "Gagné"),
        ("perdu",        "Perdu"),
    ]

    # ── Identité ──────────────────────────────────────────────────────
    prenom       = models.CharField(max_length=100, blank=True, verbose_name="Prénom")
    nom          = models.CharField(max_length=100, verbose_name="Nom / Organisation")
    email        = models.EmailField(blank=True, verbose_name="Email")
    telephone    = models.CharField(max_length=30, blank=True, verbose_name="Téléphone")
    organisation = models.CharField(max_length=200, blank=True, verbose_name="Organisation")
    lieu         = models.CharField(max_length=200, blank=True, verbose_name="Lieu / Pays")
    poste        = models.CharField(max_length=150, blank=True, verbose_name="Poste / Fonction")

    # ── Classement ────────────────────────────────────────────────────
    statut   = models.CharField(max_length=20, choices=STATUT_CHOICES, default="nouveau", verbose_name="Statut")
    pipeline = models.CharField(max_length=20, choices=PIPELINE_CHOICES, default="nouveau", verbose_name="Étape pipeline")
    tags     = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")

    # ── Commercial ────────────────────────────────────────────────────
    valeur_devis    = models.PositiveIntegerField(null=True, blank=True, verbose_name="Valeur devis (FCFA)")
    date_devis      = models.DateField(null=True, blank=True, verbose_name="Date devis")
    responsable     = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="contacts",
        verbose_name="Responsable",
    )

    # ── Source ────────────────────────────────────────────────────────
    source = models.CharField(
        max_length=20,
        choices=[
            ("site",       "Formulaire site"),
            ("telephone",  "Téléphone"),
            ("email",      "Email direct"),
            ("reseau",     "Réseau / recommandation"),
            ("evenement",  "Événement"),
            ("autre",      "Autre"),
        ],
        default="site",
        verbose_name="Source",
    )

    # ── Notes ─────────────────────────────────────────────────────────
    notes = models.TextField(blank=True, verbose_name="Notes internes")

    # ── Timestamps ────────────────────────────────────────────────────
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at  = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name        = "Contact"
        verbose_name_plural = "Contacts"
        ordering            = ["-created_at"]

    def __str__(self):
        full = f"{self.prenom} {self.nom}".strip()
        if self.organisation:
            return f"{full} — {self.organisation}"
        return full

    @property
    def initiales(self):
        parts = f"{self.prenom} {self.nom}".strip().split()
        if len(parts) >= 2:
            return f"{parts[0][0]}{parts[-1][0]}".upper()
        return self.nom[:2].upper()

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}".strip()


# ══════════════════════════════════════════════════════════════════════
# Échange / Historique
# ══════════════════════════════════════════════════════════════════════

class Echange(models.Model):

    TYPE_CHOICES = [
        ("message",    "Message reçu"),
        ("email",      "Email envoyé"),
        ("appel",      "Appel téléphonique"),
        ("reunion",    "Réunion"),
        ("devis",      "Devis envoyé"),
        ("contrat",    "Contrat signé"),
        ("livraison",  "Livraison"),
        ("note",       "Note interne"),
    ]

    contact    = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="echanges")
    type_echange = models.CharField(max_length=20, choices=TYPE_CHOICES, default="note", verbose_name="Type")
    titre      = models.CharField(max_length=200, verbose_name="Titre / Résumé")
    contenu    = models.TextField(blank=True, verbose_name="Détails")
    date       = models.DateTimeField(default=timezone.now, verbose_name="Date")
    auteur     = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="echanges",
        verbose_name="Auteur",
    )

    class Meta:
        verbose_name        = "Échange"
        verbose_name_plural = "Échanges"
        ordering            = ["-date"]

    def __str__(self):
        return f"{self.get_type_echange_display()} — {self.contact} ({self.date:%d/%m/%Y})"

    @property
    def icone(self):
        icons = {
            "message":   "ti-mail",
            "email":     "ti-send",
            "appel":     "ti-phone",
            "reunion":   "ti-users",
            "devis":     "ti-file-description",
            "contrat":   "ti-file-check",
            "livraison": "ti-package",
            "note":      "ti-note",
        }
        return icons.get(self.type_echange, "ti-circle")


# ══════════════════════════════════════════════════════════════════════
# Relance
# ══════════════════════════════════════════════════════════════════════

class Relance(models.Model):

    PRIORITE_CHOICES = [
        ("basse",   "Basse"),
        ("normale", "Normale"),
        ("haute",   "Haute"),
        ("urgente", "Urgente"),
    ]

    contact    = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="relances")
    titre      = models.CharField(max_length=200, verbose_name="Objet de la relance")
    date_prevue = models.DateField(verbose_name="Date prévue")
    priorite   = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default="normale", verbose_name="Priorité")
    effectuee  = models.BooleanField(default=False, verbose_name="Effectuée")
    notes      = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Relance"
        verbose_name_plural = "Relances"
        ordering            = ["effectuee", "date_prevue"]

    def __str__(self):
        return f"{self.contact} — {self.titre} ({self.date_prevue})"

    @property
    def est_en_retard(self):
        return not self.effectuee and self.date_prevue < timezone.now().date()

    @property
    def badge_class(self):
        if self.effectuee:
            return "rb-ok"
        if self.est_en_retard or self.priorite == "urgente":
            return "rb-urgent"
        if self.priorite == "haute":
            return "rb-soon"
        return "rb-normal"
