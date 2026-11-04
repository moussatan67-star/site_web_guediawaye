"""Recherche des coordonnées d'une adresse avec OpenStreetMap Nominatim."""

import json
import time
from decimal import Decimal
from threading import Lock
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.core.cache import cache


class GeocodingError(Exception):
    """Indique qu'une adresse n'a pas pu être convertie en coordonnées."""


_REQUEST_INTERVAL = 1.1
_last_request_time = 0.0
_request_lock = Lock()


def obtenir_coordonnees(adresse, commune):
    """Retourne la latitude et la longitude trouvées pour une adresse."""
    recherche = f"{adresse}, {commune}, Sénégal"
    cache_key = f"tourisme:coordonnees:{recherche.casefold()}"
    resultat = cache.get(cache_key)
    if resultat:
        return resultat

    global _last_request_time
    with _request_lock:
        attente = _REQUEST_INTERVAL - (time.monotonic() - _last_request_time)
        if attente > 0:
            time.sleep(attente)

        url = "https://nominatim.openstreetmap.org/search?" + urlencode(
            {"q": recherche, "format": "jsonv2", "limit": 1}
        )
        requete = Request(
            url,
            headers={"User-Agent": "GuediawayeMunicipalTourism/1.0"},
        )
        _last_request_time = time.monotonic()

        try:
            with urlopen(requete, timeout=8) as reponse:
                lieux = json.load(reponse)
        except (
            HTTPError,
            URLError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
        ) as erreur:
            raise GeocodingError(
                "OpenStreetMap n'a pas pu rechercher cette adresse. "
                "Réessayez plus tard ou saisissez les coordonnées manuellement."
            ) from erreur

    if not isinstance(lieux, list) or not lieux:
        raise GeocodingError(
            "Adresse introuvable. Précisez l'adresse ou le quartier, "
            "ou saisissez les coordonnées manuellement."
        )

    try:
        resultat = (Decimal(lieux[0]["lat"]), Decimal(lieux[0]["lon"]))
    except (KeyError, TypeError, ValueError) as erreur:
        raise GeocodingError(
            "OpenStreetMap a renvoyé des coordonnées invalides."
        ) from erreur

    cache.set(cache_key, resultat, 60 * 60 * 24 * 30)
    return resultat
