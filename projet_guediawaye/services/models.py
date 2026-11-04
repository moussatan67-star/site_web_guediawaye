"""Modèles pour les services municipaux et les demandes des citoyens."""

import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django.db import models

from core.utils import assign_unique_slug


class Service(models.Model):
    """Décrit un service proposé par la mairie."""

    nom = models.CharField("nom", max_length=160, unique=True)
    slug = models.SlugField("slug", max_length=180, unique=True, blank=True)
    description = models.TextField("description")
    photos = GenericRelation("core.PhotoGalerie", related_query_name="service")
    documents_requis = models.JSONField(
        "documents requis", default=list, blank=True,
        help_text="Liste des documents à fournir pour ce service.",
    )
    actif = models.BooleanField("actif", default=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "service municipal"
        verbose_name_plural = "services municipaux"

    def save(self, *args, **kwargs):
        if not self.slug:
            assign_unique_slug(self, self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("services:service_detail", kwargs={"slug": self.slug})


class DemandeService(models.Model):
    """Enregistre une demande de service envoyée par un citoyen."""

    # Les statuts possibles décrivent l'avancement d'une demande.
    class Statut(models.TextChoices):
        SOUMISE = "soumise", "Soumise"
        EN_COURS = "en_cours", "En cours de traitement"
        PIECES_REQUISES = "pieces_requises", "Pièces complémentaires requises"
        ACCEPTEE = "acceptee", "Acceptée"
        REFUSEE = "refusee", "Refusée"
        TERMINEE = "terminee", "Terminée"

    numero_dossier = models.UUIDField("numéro de dossier", default=uuid.uuid4, unique=True, editable=False)
    citoyen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="citoyen",
        on_delete=models.PROTECT,
        related_name="demandes_service",
        null=True,
        blank=True,
    )
    nom_demandeur = models.CharField("nom du demandeur", max_length=160, blank=True)
    email_demandeur = models.EmailField("adresse e-mail du demandeur", blank=True)
    telephone_demandeur = models.CharField("téléphone du demandeur", max_length=20, blank=True)
    service = models.ForeignKey(
        Service,
        verbose_name="service demandé",
        on_delete=models.PROTECT,
        related_name="demandes",
    )
    motif = models.TextField("motif de la demande", blank=True)
    statut = models.CharField(
        "statut", max_length=20, choices=Statut.choices, default=Statut.SOUMISE
    )
    piece_jointe = models.FileField(
        "pièce jointe",
        upload_to="demandes/pieces/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "jpg", "jpeg", "png"])],
        help_text="Formats acceptés : PDF, JPG ou PNG. Ne déposez que les pièces demandées par le service.",
    )
    reponse_mairie = models.TextField("réponse de la mairie", blank=True)
    agent_traitant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="agent traitant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="demandes_traitees",
    )
    date_creation = models.DateTimeField("date de soumission", auto_now_add=True)
    date_modification = models.DateTimeField("dernière mise à jour", auto_now=True)
    date_traitement = models.DateTimeField("date de traitement", null=True, blank=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "demande de service"
        verbose_name_plural = "demandes de service"
        indexes = [models.Index(fields=["statut", "date_creation"])]

    def __str__(self):
        return f"{self.service} — {self.numero_dossier}"


class Reclamation(models.Model):
    """Enregistre un problème signalé à la mairie par un citoyen."""

    # Les statuts possibles décrivent le traitement d'une réclamation.
    class Statut(models.TextChoices):
        SOUMISE = "soumise", "Soumise"
        EN_COURS = "en_cours", "En cours"
        REPONDUE = "repondue", "Répondue"
        CLOTUREE = "cloturee", "Clôturée"

    numero_dossier = models.UUIDField("numéro de dossier", default=uuid.uuid4, unique=True, editable=False)
    citoyen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="citoyen",
        on_delete=models.PROTECT,
        related_name="reclamations",
    )
    sujet = models.CharField("sujet", max_length=200)
    description = models.TextField("description")
    photo = models.ImageField("photo", upload_to="reclamations/", blank=True)
    statut = models.CharField(
        "statut", max_length=12, choices=Statut.choices, default=Statut.SOUMISE
    )
    reponse_mairie = models.TextField("réponse de la mairie", blank=True)
    agent_traitant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="agent traitant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reclamations_traitees",
    )
    date_creation = models.DateTimeField("date de soumission", auto_now_add=True)
    date_modification = models.DateTimeField("dernière mise à jour", auto_now=True)
    date_cloture = models.DateTimeField("date de clôture", null=True, blank=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "réclamation citoyenne"
        verbose_name_plural = "réclamations citoyennes"
        indexes = [models.Index(fields=["statut", "date_creation"])]

    def __str__(self):
        return f"{self.sujet} — {self.numero_dossier}"
