from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from core.models import Commune

from .models import EntrepriseAnnuaire


def annuaire_list(request):
    organisations = EntrepriseAnnuaire.objects.filter(valide=True).select_related("commune")
    total_organisations = organisations.count()
    recherche = request.GET.get("q", "").strip()
    secteur = request.GET.get("secteur", "")
    commune = request.GET.get("commune", "")

    if recherche:
        organisations = organisations.filter(
            Q(nom__icontains=recherche)
            | Q(description__icontains=recherche)
            | Q(adresse__icontains=recherche)
        )
    if secteur in EntrepriseAnnuaire.Secteur.values:
        organisations = organisations.filter(secteur=secteur)
    if commune:
        organisations = organisations.filter(commune__slug=commune)

    return render(
        request,
        "annuaire/list.html",
        {
            "title": "Annuaire",
            "organisations": organisations,
            "total_organisations": total_organisations,
            "communes": Commune.objects.filter(
                organisations__valide=True
            ).distinct(),
            "secteurs": EntrepriseAnnuaire.Secteur.choices,
            "recherche": recherche,
            "secteur_selectionne": secteur,
            "commune_selectionnee": commune,
        },
    )


def entreprise_detail(request, slug):
    organisation = get_object_or_404(
        EntrepriseAnnuaire.objects.select_related('commune'),
        slug=slug,
        valide=True,
    )
    return render(
        request,
        'annuaire/detail.html',
        {'title': organisation.nom, 'organisation': organisation},
    )
