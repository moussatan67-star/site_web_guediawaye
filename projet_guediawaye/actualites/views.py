from django.shortcuts import get_object_or_404, render

from .models import Actualite


def actualites_list(request):
    articles = Actualite.objects.filter(statut=Actualite.Statut.PUBLIEE).select_related('auteur')
    return render(
        request,
        'actualites/list.html',
        {'title': 'Actualités', 'articles': articles},
    )


def actualite_detail(request, slug):
    article = get_object_or_404(
        Actualite.objects.select_related('auteur'),
        slug=slug,
        statut=Actualite.Statut.PUBLIEE,
    )
    return render(
        request,
        'actualites/detail.html',
        {'title': article.titre, 'article': article},
    )
