from django import forms
from django.core.exceptions import ValidationError

from .geocoding import GeocodingError, obtenir_coordonnees
from .models import LieuTouristique


class LieuTouristiqueAdminForm(forms.ModelForm):
    class Meta:
        model = LieuTouristique
        fields = "__all__"
        help_texts = {
            "adresse": (
                "Indiquez l'adresse ou le quartier pour trouver automatiquement "
                "les coordonnées avec OpenStreetMap."
            ),
        }

    def clean(self):
        donnees = super().clean()
        adresse = donnees.get("adresse")
        commune = donnees.get("commune")
        latitude = donnees.get("latitude")
        longitude = donnees.get("longitude")

        if (latitude is None) != (longitude is None):
            raise ValidationError(
                "Renseignez les deux coordonnées ou laissez les deux champs vides."
            )

        adresse_modifiee = (
            self.instance.pk
            and (
                adresse != self.instance.adresse
                or commune != self.instance.commune
            )
            and latitude == self.instance.latitude
            and longitude == self.instance.longitude
        )
        if adresse_modifiee:
            latitude = None
            longitude = None

        if latitude is None and longitude is None and adresse and commune:
            try:
                donnees["latitude"], donnees["longitude"] = obtenir_coordonnees(
                    adresse, commune.nom
                )
            except GeocodingError as erreur:
                self.add_error("adresse", str(erreur))

        return donnees
