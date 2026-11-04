"""Modèles partagés par les différentes rubriques du site."""

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .utils import assign_unique_slug


class Commune(models.Model):
    """Décrit une commune et ses informations générales."""

    nom = models.CharField("nom", max_length=100, unique=True)
    slug = models.SlugField("slug", max_length=120, unique=True, blank=True)
    description = models.TextField("description", blank=True)
    quartiers = models.TextField(
        "quartiers", blank=True, help_text="Liste des quartiers, séparés par des virgules."
    )
    population = models.PositiveIntegerField("population", null=True, blank=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "commune"
        verbose_name_plural = "communes"

    def save(self, *args, **kwargs):
        if not self.slug:
            assign_unique_slug(self, self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Contact(models.Model):
    """Enregistre un message envoyé depuis le formulaire de contact."""

    nom = models.CharField("nom", max_length=150)
    email = models.EmailField("adresse e-mail")
    sujet = models.CharField("sujet", max_length=200)
    message = models.TextField("message")
    traite = models.BooleanField("traité", default=False)
    date_creation = models.DateTimeField("date de réception", auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]
        verbose_name = "message de contact"
        verbose_name_plural = "messages de contact"

    def __str__(self):
        return f"{self.sujet} — {self.nom}"


class PageInstitutionnelle(models.Model):
    """Contient une page d'information sur la mairie ou la commune."""

    # Ce choix précise le type de page institutionnelle.
    class TypePage(models.TextChoices):
        A_PROPOS = "a-propos", "À propos"
        MOT_DU_MAIRE = "mot-du-maire", "Mot du maire"
        ORGANIGRAMME = "organigramme", "Organigramme"
        HISTOIRE = "histoire", "Histoire"

    titre = models.CharField("titre", max_length=200)
    slug = models.SlugField("slug", max_length=220, unique=True, blank=True)
    type_page = models.CharField("type de page", max_length=30, choices=TypePage.choices)
    contenu = models.TextField("contenu")
    publiee = models.BooleanField("publiée", default=True)
    ordre = models.PositiveSmallIntegerField("ordre d'affichage", default=0)
    date_modification = models.DateTimeField("dernière modification", auto_now=True)
    photos = GenericRelation("core.PhotoGalerie", related_query_name="page_institutionnelle")

    class Meta:
        ordering = ["ordre", "titre"]
        verbose_name = "page institutionnelle"
        verbose_name_plural = "pages institutionnelles"

    def save(self, *args, **kwargs):
        if not self.slug:
            assign_unique_slug(self, self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


class PhotoGalerie(models.Model):
    """Associe une photo à différents types de contenu du site."""

    # Cette relation permet à une photo d'appartenir à plusieurs modèles.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    image = models.ImageField("photo", upload_to="galeries/")
    legende = models.CharField("légende", max_length=180, blank=True)
    ordre = models.PositiveSmallIntegerField("ordre d'affichage", default=0)

    class Meta:
        ordering = ["ordre", "pk"]
        verbose_name = "photo de galerie"
        verbose_name_plural = "photos de galerie"
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def __str__(self):
        return self.legende or self.image.name


class PartenaireInstitutionnel(models.Model):
    """Enregistre un partenaire et les informations de son site web."""

    nom = models.CharField("nom", max_length=150)
    logo = models.ImageField("logo", upload_to="partenaires/", blank=True)
    site_web = models.URLField("site web", blank=True)
    actif = models.BooleanField("actif", default=True)
    ordre = models.PositiveSmallIntegerField("ordre d'affichage", default=0)

    class Meta:
        ordering = ["ordre", "nom"]
        verbose_name = "partenaire institutionnel"
        verbose_name_plural = "partenaires institutionnels"

    def __str__(self):
        return self.nom


class FAQ(models.Model):
    """Enregistre une question fréquente et sa réponse."""

    question = models.CharField("question", max_length=300)
    reponse = models.TextField("réponse")
    categorie = models.CharField("catégorie", max_length=100, blank=True)
    publiee = models.BooleanField("publiée", default=True)
    ordre = models.PositiveSmallIntegerField("ordre d'affichage", default=0)

    class Meta:
        ordering = ["categorie", "ordre", "question"]
        verbose_name = "foire aux questions"
        verbose_name_plural = "foire aux questions"

    def __str__(self):
        return self.question


class Newsletter(models.Model):
    """Enregistre l'adresse e-mail d'un abonné à la newsletter."""

    email = models.EmailField("adresse e-mail", unique=True)
    date_inscription = models.DateTimeField("date d'inscription", auto_now_add=True)
    actif = models.BooleanField("abonnement actif", default=True)

    class Meta:
        ordering = ["-date_inscription"]
        verbose_name = "abonné à la newsletter"
        verbose_name_plural = "abonnés à la newsletter"

    def __str__(self):
        return self.email
