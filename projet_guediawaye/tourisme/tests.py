from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.utils import timezone

from core.models import Commune, PhotoGalerie

from .forms import LieuTouristiqueAdminForm
from .models import EvenementCulturel, LieuTouristique
from .views import tourisme_list


class LieuTouristiqueTests(TestCase):
    def setUp(self):
        self.commune = Commune.objects.create(nom="Guédiawaye")

    @patch("tourisme.forms.obtenir_coordonnees")
    def test_address_generates_coordinates_automatically(self, obtenir_coordonnees):
        obtenir_coordonnees.return_value = (Decimal("14.7761"), Decimal("-17.3956"))
        formulaire = LieuTouristiqueAdminForm(
            data={
                "nom": "Parc municipal",
                "categorie": LieuTouristique.Categorie.NATURE,
                "description": "Un espace vert de la commune.",
                "adresse": "Centre-ville",
                "commune": self.commune.pk,
            }
        )

        self.assertTrue(formulaire.is_valid(), formulaire.errors)
        lieu = formulaire.save()

        self.assertEqual(lieu.latitude, Decimal("14.7761"))
        self.assertEqual(lieu.longitude, Decimal("-17.3956"))
        obtenir_coordonnees.assert_called_once_with("Centre-ville", "Guédiawaye")

    @patch("tourisme.forms.obtenir_coordonnees")
    def test_manual_coordinates_are_kept(self, obtenir_coordonnees):
        formulaire = LieuTouristiqueAdminForm(
            data={
                "nom": "Mairie",
                "categorie": LieuTouristique.Categorie.PATRIMOINE,
                "description": "La mairie de la commune.",
                "adresse": "Guédiawaye",
                "latitude": "14.776100",
                "longitude": "-17.395600",
                "commune": self.commune.pk,
            }
        )

        self.assertTrue(formulaire.is_valid(), formulaire.errors)
        lieu = formulaire.save()

        self.assertEqual(lieu.get_categorie_display(), "Patrimoine")
        obtenir_coordonnees.assert_not_called()


class EvenementCulturelTests(TestCase):
    def test_tourism_page_shows_upcoming_event_and_its_gallery(self):
        debut = timezone.now() + timedelta(days=2)
        evenement = EvenementCulturel.objects.create(
            titre="Festival culturel",
            description="Une rencontre autour des arts et de la culture.",
            date_debut=debut,
            date_fin=debut + timedelta(hours=4),
            publie=True,
        )
        PhotoGalerie.objects.create(
            content_object=evenement,
            image="galeries/festival.jpg",
            legende="Scène du festival",
        )
        evenement_passe = EvenementCulturel.objects.create(
            titre="Ancien événement",
            description="Cet événement est terminé.",
            date_debut=timezone.now() - timedelta(days=4),
            date_fin=timezone.now() - timedelta(days=3),
            publie=True,
        )

        request = RequestFactory().get("/tourisme/")
        request.user = AnonymousUser()
        response = tourisme_list(request)
        contenu = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn("Festival culturel", contenu)
        self.assertIn("Scène du festival", contenu)
        self.assertIn("/media/galeries/festival.jpg", contenu)
        self.assertNotIn("Ancien événement", contenu)
