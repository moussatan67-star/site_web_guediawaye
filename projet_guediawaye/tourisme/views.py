from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import EvenementCulturel, LieuTouristique


def tourisme_list(request):
    lieux = LieuTouristique.objects.filter(publie=True).select_related('commune')
    evenements = EvenementCulturel.objects.filter(
        publie=True, date_fin__gte=timezone.now()
    ).select_related('lieu').prefetch_related('photos')
    return render(
        request,
        'tourisme/list.html',
        {'title': 'Tourisme', 'lieux': lieux, 'evenements': evenements},
    )


def tourisme_detail(request, slug):
    lieu = get_object_or_404(
        LieuTouristique.objects.select_related('commune'),
        slug=slug,
        publie=True,
    )
    evenements = lieu.evenements.filter(publie=True).prefetch_related('photos')
    return render(
        request,
        'tourisme/detail.html',
        {'title': lieu.nom, 'lieu': lieu, 'evenements': evenements},
    )
