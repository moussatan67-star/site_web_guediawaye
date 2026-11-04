"""Modèles pour les actualités publiées par la commune."""

from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.db import models
from django.utils import timezone

from core.utils import assign_unique_slug


class Actualite(models.Model):
    """Contient une actualité, son auteur et son état de publication."""

    class Categorie(models.TextChoices):
        VIE_COMMUNALE = "vie_communale", "Vie communale"
        SERVICES = "services", "Services municipaux"
        EDUCATION = "education", "Éducation"
        SANTE = "sante", "Santé"
        CULTURE_SPORT = "culture_sport", "Culture et sport"
        ENVIRONNEMENT = "environnement", "Environnement"
        ECONOMIE = "economie", "Économie et emploi"
        ANNONCES = "annonces", "Annonces"
        AUTRE = "autre", "Autre"

    # TextChoices associe une valeur enregistrée en base à un libellé lisible.
    class Statut(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        PUBLIEE = "publiee", "Publiée"
        ARCHIVEE = "archivee", "Archivée"

    titre = models.CharField("titre", max_length=200)
    slug = models.SlugField("slug", max_length=220, unique=True, blank=True)
    contenu = models.TextField("contenu")
    image = models.ImageField("image", upload_to="actualites/", blank=True)
    photos = GenericRelation("core.PhotoGalerie", related_query_name="actualite")
    categorie = models.CharField(
        "catégorie",
        max_length=20,
        choices=Categorie.choices,
        default=Categorie.VIE_COMMUNALE,
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="auteur",
        on_delete=models.SET_NULL,
        null=True,
        related_name="actualites_redigees",
    )
    statut = models.CharField(
        "statut", max_length=12, choices=Statut.choices, default=Statut.BROUILLON
    )
    date_creation = models.DateTimeField("date de création", auto_now_add=True)
    date_publication = models.DateTimeField(
        "date de publication",
        default=timezone.now,
        null=True,
        blank=True,
    )
    date_modification = models.DateTimeField("dernière modification", auto_now=True)

    class Meta:
        ordering = ["-date_publication", "-date_creation"]
        verbose_name = "actualité"
        verbose_name_plural = "actualités"
        indexes = [models.Index(fields=["statut", "date_publication"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            assign_unique_slug(self, self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("actualites:actualite_detail", kwargs={"slug": self.slug})
