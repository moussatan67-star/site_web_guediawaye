import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_senegalais(value):
    if value and not re.fullmatch(r"\+221\d{9}", value):
        raise ValidationError(
            _("Saisissez un numéro sénégalais au format +221XXXXXXXXX.")
        )


def validate_cni_senegalaise(value):
    if value and not re.fullmatch(r"[A-Za-z0-9]{9,17}", value):
        raise ValidationError(
            _("Le numéro de CNI doit contenir de 9 à 17 caractères alphanumériques.")
        )
