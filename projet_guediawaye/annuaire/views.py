from django.shortcuts import get_object_or_404, render

from .models import EntrepriseAnnuaire


def annuaire_list(request):
    organisations = EntrepriseAnnuaire.objects.filter(valide=True).select_related('commune')
    return render(
        request,
        'annuaire/list.html',
        {'title': 'Annuaire', 'organisations': organisations},
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
