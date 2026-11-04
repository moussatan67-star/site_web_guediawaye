"""Modèle des entreprises, associations et autres acteurs locaux."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from core.utils import assign_unique_slug


class EntrepriseAnnuaire(models.Model):
    """Décrit une organisation inscrite dans l'annuaire communal."""

    # Les secteurs possibles sont limités à ces valeurs.
    class Secteur(models.TextChoices):
        COMMERCE = "commerce", "Commerce"
        ARTISANAT = "artisanat", "Artisanat"
        SERVICES = "services", "Services"
        INDUSTRIE = "industrie", "Industrie"
        ASSOCIATION = "association", "Association"
        AUTRE = "autre", "Autre"

    nom = models.CharField("nom", max_length=180)
    slug = models.SlugField("slug", max_length=200, unique=True, blank=True)
    secteur = models.CharField("secteur", max_length=20, choices=Secteur.choices)
    description = models.TextField("description", blank=True)
    telephone = models.CharField("téléphone", max_length=30, blank=True)
    email = models.EmailField("adresse e-mail", blank=True)
    adresse = models.CharField("adresse", max_length=255)
    commune = models.ForeignKey(
        "core.Commune",
        verbose_name="commune",
        on_delete=models.PROTECT,
        related_name="organisations",
    )
    logo = models.ImageField("logo", upload_to="annuaire/logos/", blank=True)
    photos = GenericRelation("core.PhotoGalerie", related_query_name="organisation")
    site_web = models.URLField("site web", blank=True)
    valide = models.BooleanField("validé par la mairie", default=False)
    date_creation = models.DateTimeField("date de soumission", auto_now_add=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "organisation de l'annuaire"
        verbose_name_plural = "organisations de l'annuaire"
        indexes = [models.Index(fields=["secteur", "valide"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            assign_unique_slug(self, self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("annuaire:entreprise_detail", kwargs={"slug": self.slug})
