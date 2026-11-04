from django.test import TestCase

from actualites.models import Actualite

from .models import Commune, PageInstitutionnelle, PhotoGalerie


class CommuneSeedTests(TestCase):
    def test_arrondissement_communes_are_available(self):
        communes = set(Commune.objects.values_list("nom", flat=True))

        self.assertTrue(
            {
                "Golf Sud",
                "Médina Gounass",
                "Ndiarème Limamoulaye",
                "Sam Notaire",
                "Wakhinane-Nimzatt",
            }.issubset(communes)
        )


class HomePageTests(TestCase):
    def test_homepage_displays_published_news_and_category(self):
        Actualite.objects.create(
            titre="Annonce de la commune",
            contenu="Une information importante.",
            categorie=Actualite.Categorie.ANNONCES,
            statut=Actualite.Statut.PUBLIEE,
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Annonce de la commune")
        self.assertContains(response, "Annonces")


class PhotoGalerieTests(TestCase):
    def test_multiple_photos_can_be_attached_to_an_institutional_page(self):
        page = PageInstitutionnelle.objects.create(
            titre="À propos de la commune",
            type_page=PageInstitutionnelle.TypePage.A_PROPOS,
            contenu="Informations institutionnelles.",
        )
        premiere_photo = PhotoGalerie.objects.create(
            content_object=page,
            image="galeries/mairie-1.jpg",
            legende="Vue de la mairie",
            ordre=1,
        )
        deuxieme_photo = PhotoGalerie.objects.create(
            content_object=page,
            image="galeries/mairie-2.jpg",
            legende="Accueil du public",
            ordre=2,
        )

        self.assertEqual(list(page.photos.all()), [premiere_photo, deuxieme_photo])
