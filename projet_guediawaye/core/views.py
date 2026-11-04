from django.shortcuts import render

from actualites.models import Actualite


def home(request):
    articles = Actualite.objects.filter(
        statut=Actualite.Statut.PUBLIEE
    ).select_related('auteur')[:3]
    return render(
        request,
        'core/home.html',
        {'title': 'Accueil', 'articles': articles},
    )


def contact(request):
    return render(request, 'core/contact.html', {'title': 'Contact'})
