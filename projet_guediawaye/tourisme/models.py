"""Modèles pour les lieux touristiques et les événements culturels."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from core.utils import assign_unique_slug


class LieuTouristique(models.Model):
    """Décrit un lieu à visiter dans une commune."""

    class Categorie(models.TextChoices):
        PATRIMOINE = "patrimoine", "Patrimoine"
        CULTURE = "culture", "Culture"
        NATURE = "nature", "Nature"
        LOISIRS = "loisirs", "Loisirs"
        RESTAURATION = "restauration", "Restauration"
        HEBERGEMENT = "hebergement", "Hébergement"
        AUTRE = "autre", "Autre"

    nom = models.CharField("nom", max_length=180)
    slug = models.SlugField("slug", max_length=200, unique=True, blank=True)
    categorie = models.CharField(
        "catégorie",
        max_length=20,
        choices=Categorie.choices,
        default=Categorie.AUTRE,
    )
    description = models.TextField("description")
    adresse = models.CharField("adresse ou quartier", max_length=255, blank=True)
    photo = models.ImageField("photo principale", upload_to="tourisme/lieux/", blank=True)
    photos = GenericRelation("core.PhotoGalerie", related_query_name="lieu_touristique")
    latitude = models.DecimalField("latitude", max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField("longitude", max_digits=9, decimal_places=6, null=True, blank=True)
    commune = models.ForeignKey(
        "core.Commune",
        verbose_name="commune",
        on_delete=models.PROTECT,
        related_name="lieux_touristiques",
    )
    publie = models.BooleanField("publié", default=False)

    class Meta:
        ordering = ["nom"]
        verbose_name = "lieu touristique"
        verbose_name_plural = "lieux touristiques"

    def save(self, *args, **kwargs):
        if not self.slug:
            assign_unique_slug(self, self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("tourisme:tourisme_detail", kwargs={"slug": self.slug})


class EvenementCulturel(models.Model):
    """Décrit un événement culturel et ses dates."""

    titre = models.CharField("titre", max_length=200)
    slug = models.SlugField("slug", max_length=220, unique=True, blank=True)
    description = models.TextField("description")
    date_debut = models.DateTimeField("date de début")
    date_fin = models.DateTimeField("date de fin")
    photos = GenericRelation("core.PhotoGalerie", related_query_name="evenement_culturel")
    lieu = models.ForeignKey(
        LieuTouristique,
        verbose_name="lieu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evenements",
    )
    image = models.ImageField("image", upload_to="tourisme/evenements/", blank=True)
    publie = models.BooleanField("publié", default=False)
    date_creation = models.DateTimeField("date de création", auto_now_add=True)

    class Meta:
        ordering = ["date_debut"]
        verbose_name = "événement culturel"
        verbose_name_plural = "événements culturels"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(date_fin__gte=models.F("date_debut")),
                name="evenement_date_fin_apres_debut",
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            assign_unique_slug(self, self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre
