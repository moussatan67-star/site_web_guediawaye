from django.test import TestCase
from django.urls import reverse

from core.models import Commune

from .models import EntrepriseAnnuaire


class AnnuaireTests(TestCase):
    def setUp(self):
        self.commune = Commune.objects.create(nom="Commune de test")
        self.autre_commune = Commune.objects.create(nom="Autre commune")
        self.commerce = EntrepriseAnnuaire.objects.create(
            nom="Boulangerie de test",
            secteur=EntrepriseAnnuaire.Secteur.COMMERCE,
            description="Pain et pâtisseries",
            adresse="Quartier de test",
            commune=self.commune,
            valide=True,
        )
        self.association = EntrepriseAnnuaire.objects.create(
            nom="Association sportive",
            secteur=EntrepriseAnnuaire.Secteur.ASSOCIATION,
            description="Activités sportives locales",
            adresse="Autre quartier",
            commune=self.autre_commune,
            valide=True,
        )
        EntrepriseAnnuaire.objects.create(
            nom="Structure non publiée",
            secteur=EntrepriseAnnuaire.Secteur.SERVICES,
            adresse="Adresse de test",
            commune=self.commune,
            valide=False,
        )
        self.url = reverse("annuaire:annuaire_list")

    def test_annuaire_affiche_uniquement_les_structures_validees(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.commerce.nom)
        self.assertContains(response, self.association.nom)
        self.assertNotContains(response, "Structure non publiée")
        self.assertEqual(response.context["total_organisations"], 2)

    def test_recherche_filtre_par_nom_description_et_adresse(self):
        response = self.client.get(self.url, {"q": "pâtisseries"})

        self.assertContains(response, self.commerce.nom)
        self.assertNotContains(response, self.association.nom)

    def test_filtres_secteur_et_commune_peuvent_etre_combines(self):
        response = self.client.get(
            self.url,
            {
                "secteur": EntrepriseAnnuaire.Secteur.COMMERCE,
                "commune": self.commune.slug,
            },
        )

        self.assertContains(response, self.commerce.nom)
        self.assertNotContains(response, self.association.nom)

    def test_fiche_non_validee_reste_inaccessible(self):
        response = self.client.get(
            reverse(
                "annuaire:entreprise_detail",
                kwargs={"slug": "structure-non-publiee"},
            )
        )

        self.assertEqual(response.status_code, 404)
