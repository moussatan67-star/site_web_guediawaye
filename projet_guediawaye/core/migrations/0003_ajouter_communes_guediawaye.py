from django.db import migrations
from django.utils.text import slugify


COMMUNES = [
    "Golf Sud",
    "Médina Gounass",
    "Ndiarème Limamoulaye",
    "Sam Notaire",
    "Wakhinane-Nimzatt",
]


def ajouter_communes(apps, schema_editor):
    Commune = apps.get_model("core", "Commune")
    for nom in COMMUNES:
        Commune.objects.using(schema_editor.connection.alias).get_or_create(
            nom=nom,
            defaults={"slug": slugify(nom)},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_photogalerie"),
    ]

    operations = [
        migrations.RunPython(ajouter_communes, migrations.RunPython.noop),
    ]
