from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import DemandeService, Service


class DemandeServiceTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            nom="État civil",
            description="Démarches d'état civil.",
        )
        self.url = reverse("services:service_demande", kwargs={"slug": self.service.slug})

    def test_public_can_submit_a_service_request(self):
        response = self.client.post(
            self.url,
            {
                "nom_demandeur": "Awa Ndiaye",
                "email_demandeur": "awa@example.com",
                "telephone_demandeur": "+221771234567",
                "motif": "Je souhaite obtenir un acte de naissance.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/demande_confirmation.html")
        demande = DemandeService.objects.get()
        self.assertIsNone(demande.citoyen)
        self.assertEqual(demande.service, self.service)
        self.assertEqual(demande.nom_demandeur, "Awa Ndiaye")
        self.assertEqual(demande.motif, "Je souhaite obtenir un acte de naissance.")
        self.assertContains(response, str(demande.numero_dossier))

    def test_authenticated_request_is_linked_to_the_account(self):
        citoyen = get_user_model().objects.create_user(
            username="awa",
            password="test-password",
            email="awa@example.com",
        )
        self.client.force_login(citoyen)

        response = self.client.post(
            self.url,
            {
                "nom_demandeur": "Awa Ndiaye",
                "email_demandeur": "awa@example.com",
                "telephone_demandeur": "+221771234567",
                "motif": "Je souhaite obtenir un acte de naissance.",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(DemandeService.objects.get().citoyen, citoyen)

    def test_request_requires_contact_details_and_a_motif(self):
        response = self.client.post(
            self.url,
            {
                "nom_demandeur": "",
                "email_demandeur": "",
                "telephone_demandeur": "",
                "motif": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/demande_form.html")
        self.assertEqual(DemandeService.objects.count(), 0)

    def test_inactive_service_cannot_receive_requests(self):
        self.service.actif = False
        self.service.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_upload_rejects_unsupported_file_extensions(self):
        response = self.client.post(
            self.url,
            {
                "nom_demandeur": "Awa Ndiaye",
                "email_demandeur": "awa@example.com",
                "telephone_demandeur": "+221771234567",
                "motif": "Je souhaite obtenir un acte de naissance.",
                "piece_jointe": SimpleUploadedFile("document.exe", b"contenu"),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "services/demande_form.html")
        self.assertEqual(DemandeService.objects.count(), 0)
