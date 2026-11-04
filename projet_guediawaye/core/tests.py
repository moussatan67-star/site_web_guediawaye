from django.test import TestCase

from actualites.models import Actualite

from .models import Commune, Contact, PageInstitutionnelle, PhotoGalerie


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


class ContactPageTests(TestCase):
    def test_contact_page_displays_form_and_reduced_map(self):
        response = self.client.get("/contact/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="nom"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="sujet"')
        self.assertContains(response, 'name="message"')
        self.assertContains(response, "openstreetmap.org/export/embed.html")

    def test_valid_contact_submission_is_saved(self):
        response = self.client.post(
            "/contact/",
            {
                "nom": "Awa Diop",
                "email": "awa@example.com",
                "sujet": "Question",
                "message": "Bonjour, je souhaite une information.",
            },
        )

        self.assertRedirects(response, "/contact/")
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.get()
        self.assertEqual(contact.nom, "Awa Diop")
        self.assertEqual(contact.email, "awa@example.com")
        self.assertEqual(contact.sujet, "Question")
        self.assertEqual(contact.message, "Bonjour, je souhaite une information.")

    def test_invalid_contact_submission_is_not_saved(self):
        response = self.client.post(
            "/contact/",
            {
                "nom": "Awa Diop",
                "email": "adresse-invalide",
                "sujet": "Question",
                "message": "Bonjour.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(Contact.objects.count(), 0)


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
