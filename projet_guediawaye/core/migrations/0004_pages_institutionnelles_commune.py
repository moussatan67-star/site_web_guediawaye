from django.db import migrations


PAGES = [
    {
        "titre": "Histoire de Guédiawaye",
        "slug": "histoire",
        "type_page": "histoire",
        "ordre": 1,
        "contenu": (
            "Guédiawaye s’est développée avec l’extension de l’agglomération de Dakar. "
            "Au fil du temps, le territoire est devenu un centre urbain à part entière, "
            "avec une vie de quartier, des activités économiques et des initiatives "
            "portées par ses habitants.\n\n"
            "L’organisation communale actuelle réunit cinq communes : Golf Sud, "
            "Médina Gounass, Ndiarème Limamoulaye, Sam Notaire et Wakhinane-Nimzatt. "
            "Cette organisation rapproche les services publics des habitants et "
            "accompagne le développement de la ville.\n\n"
            "Les repères chronologiques détaillés seront ajoutés à cette page à mesure "
            "qu’ils seront confirmés à partir des archives et des sources officielles "
            "de la commune."
        ),
    },
    {
        "titre": "À propos de la commune",
        "slug": "a-propos",
        "type_page": "a-propos",
        "ordre": 2,
        "contenu": (
            "Guédiawaye est une ville de la région de Dakar, au Sénégal. Son territoire "
            "est organisé autour de cinq communes : Golf Sud, Médina Gounass, "
            "Ndiarème Limamoulaye, Sam Notaire et Wakhinane-Nimzatt.\n\n"
            "Ce portail rassemble les informations communales, les services municipaux, "
            "les actualités, les ressources locales et les informations culturelles "
            "publiées. Il a pour objectif de faciliter l’accès des habitants aux "
            "rubriques et aux renseignements disponibles."
        ),
    },
]


def ajouter_pages_institutionnelles(apps, schema_editor):
    PageInstitutionnelle = apps.get_model("core", "PageInstitutionnelle")
    manager = PageInstitutionnelle.objects.using(schema_editor.connection.alias)
    for page in PAGES:
        manager.get_or_create(
            slug=page["slug"],
            defaults={
                "titre": page["titre"],
                "type_page": page["type_page"],
                "contenu": page["contenu"],
                "publiee": True,
                "ordre": page["ordre"],
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_ajouter_communes_guediawaye"),
    ]

    operations = [
        migrations.RunPython(
            ajouter_pages_institutionnelles,
            migrations.RunPython.noop,
        ),
    ]
