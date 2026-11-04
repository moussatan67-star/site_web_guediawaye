"""Modèle du compte utilisateur et de ses informations communales."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_cni_senegalaise, validate_phone_senegalais


class User(AbstractUser):
    """Ajoute le rôle et les coordonnées d'un utilisateur du site."""

    # Les rôles possibles sont limités à ces valeurs.
    class Role(models.TextChoices):
        CITOYEN = "citoyen", "Citoyen"
        AGENT = "agent", "Agent municipal"
        ADMINISTRATEUR = "administrateur", "Administrateur"

    role = models.CharField("rôle", max_length=20, choices=Role.choices, default=Role.CITOYEN)
    telephone = models.CharField(
        "téléphone",
        max_length=13,
        blank=True,
        validators=[validate_phone_senegalais],
        help_text="Format international : +221 suivi des 9 chiffres.",
    )
    numero_cni = models.CharField(
        "numéro CNI",
        max_length=17,
        blank=True,
        validators=[validate_cni_senegalaise],
    )
    adresse = models.CharField("adresse", max_length=255, blank=True)
    commune = models.ForeignKey(
        "core.Commune",
        verbose_name="commune de résidence",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="residents",
    )

    class Meta:
        ordering = ["last_name", "first_name", "username"]
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"

    def __str__(self):
        return self.get_full_name() or self.username
