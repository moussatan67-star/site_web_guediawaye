from django.db import migrations
from django.utils.text import slugify


SERVICES = [
    (
        "État civil",
        "Accueil et orientation pour les démarches d’état civil, notamment les actes de naissance, de mariage et de décès. Les pièces à fournir et les modalités dépendent de la démarche.",
    ),
    (
        "Urbanisme et occupation du domaine public",
        "Information et orientation concernant les questions d’urbanisme et les demandes liées à l’occupation du domaine public communal. Les autorisations et pièces nécessaires sont à confirmer auprès du service.",
    ),
    (
        "Hygiène et assainissement",
        "Signalement et orientation des demandes relatives à la propreté, à l’assainissement et à l’hygiène du cadre de vie dans la commune.",
    ),
    (
        "Voirie et éclairage public",
        "Transmission des signalements et demandes concernant la voirie et l’éclairage public, pour orientation vers le service compétent.",
    ),
    (
        "Environnement et cadre de vie",
        "Information et orientation sur les initiatives et demandes liées à la protection de l’environnement et à l’amélioration du cadre de vie.",
    ),
    (
        "Action sociale et solidarité",
        "Accueil et orientation des habitants qui souhaitent se renseigner sur l’accompagnement social et les dispositifs de solidarité disponibles.",
    ),
    (
        "Éducation et petite enfance",
        "Information et orientation concernant les actions communales en matière d’éducation et de petite enfance. Les modalités varient selon le dispositif.",
    ),
    (
        "Jeunesse, sports et culture",
        "Renseignements et orientation concernant les activités, initiatives et équipements communaux dédiés à la jeunesse, au sport et à la culture.",
    ),
    (
        "Développement local et vie économique",
        "Information et orientation sur les initiatives communales qui contribuent au développement local et à la vie économique.",
    ),
    (
        "Accueil et orientation des citoyens",
        "Point d’accueil pour être orienté vers le service municipal compétent et obtenir des renseignements généraux sur les démarches.",
    ),
]


def ajouter_services(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    for nom, description in SERVICES:
        Service.objects.get_or_create(
            nom=nom,
            defaults={
                "description": description,
                "slug": slugify(nom),
                "documents_requis": [],
                "actif": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0002_demandeservice_email_demandeur_demandeservice_motif_and_more"),
    ]

    operations = [
        migrations.RunPython(ajouter_services, migrations.RunPython.noop),
    ]
