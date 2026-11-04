from datetime import datetime, timezone as datetime_timezone

from django.test import RequestFactory, TestCase

from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import PhotoGalerie

from .models import Actualite
from .views import actualite_detail


class ActualiteDateTests(TestCase):
    def test_publication_date_is_filled_automatically(self):
        article = Actualite.objects.create(
            titre="Actualité avec date automatique",
            contenu="Contenu de test.",
        )

        self.assertIsNotNone(article.date_publication)
        self.assertLess((timezone.now() - article.date_publication).total_seconds(), 5)

    def test_publication_date_can_be_changed_manually(self):
        date_choisie = datetime(2025, 1, 15, 10, 30, tzinfo=datetime_timezone.utc)
        article = Actualite.objects.create(
            titre="Actualité avec date choisie",
            contenu="Contenu de test.",
            date_publication=date_choisie,
        )

        self.assertEqual(article.date_publication, date_choisie)


class ActualiteGalleryTests(TestCase):
    def test_category_has_a_readable_label(self):
        article = Actualite.objects.create(
            titre="Une actualité locale",
            contenu="Informations locales.",
            categorie=Actualite.Categorie.CULTURE_SPORT,
        )

        self.assertEqual(article.get_categorie_display(), "Culture et sport")

    def test_detail_page_displays_every_gallery_photo(self):
        auteur = get_user_model().objects.create_user(
            username="redacteur",
            password="test-password",
        )
        article = Actualite.objects.create(
            titre="Une actualité locale",
            contenu="Informations détaillées sur cette actualité.",
            auteur=auteur,
            statut=Actualite.Statut.PUBLIEE,
        )
        PhotoGalerie.objects.create(
            content_object=article,
            image="galeries/actualite-1.jpg",
            legende="Première photo",
        )
        PhotoGalerie.objects.create(
            content_object=article,
            image="galeries/actualite-2.jpg",
            legende="Deuxième photo",
        )

        request = RequestFactory().get(article.get_absolute_url())
        request.user = auteur
        response = actualite_detail(request, slug=article.slug)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/media/galeries/actualite-1.jpg")
        self.assertContains(response, "/media/galeries/actualite-2.jpg")
        self.assertContains(response, "Première photo")
        self.assertContains(response, "Deuxième photo")
