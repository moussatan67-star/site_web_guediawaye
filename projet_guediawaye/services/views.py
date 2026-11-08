from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import DemandeServiceForm
from .models import Service


DEFAULT_SERVICE_ILLUSTRATION = {
    "image": None,
    "alt": "",
    "caption": "",
}

SERVICE_ILLUSTRATIONS = {
    "accueil-et-orientation-des-citoyens": {
        "image": "images/mairie.jpg",
        "alt": "Place publique aménagée à Guédiawaye",
        "caption": "Espace public de Guédiawaye",
    },
    "etat-civil": {
        "image": "images/fbtgotgj.jpg",
        "alt": "Façade de l’Hôtel de Ville de Guédiawaye",
        "caption": "Hôtel de Ville de Guédiawaye",
    },
    "developpement-local-et-vie-economique": {
        "image": "images/ARTISANT.jpg",
        "alt": "Boutique d’artisanat au Sénégal",
        "caption": "Artisanat et savoir-faire locaux",
    },
    "environnement-et-cadre-de-vie": {
        "image": "images/V.jpg",
        "alt": "Vue aérienne de la plage de Malibu au Sénégal",
        "caption": "Littoral sénégalais",
    },
    "hygiene-et-assainissement": {
        "image": "images/commerce.jpg",
        "alt": "Marché animé au Sénégal",
        "caption": "Marché et espace public",
    },
    "jeunesse-sports-et-culture": {
        "image": "images/STADE.jpg",
        "alt": "Stade aux couleurs du Sénégal",
        "caption": "Sport et jeunesse au Sénégal",
    },
    "mairiedes-commun": {
        "image": "images/JOJ.jpg",
        "alt": "Cérémonie officielle au Sénégal",
        "caption": "Équipement public et vie communale",
    },
    "urbanisme-et-occupation-du-domaine-public": {
        "image": "images (2).jpg",
        "alt": "Vue aérienne d’un quartier sénégalais",
        "caption": "Vue urbaine au Sénégal",
    },
}


def _attach_illustration(service):
    service.illustration = SERVICE_ILLUSTRATIONS.get(
        service.slug, DEFAULT_SERVICE_ILLUSTRATION
    )
    return service


def services_list(request):
    services = Service.objects.filter(actif=True)
    total_services = services.count()
    recherche = request.GET.get("q", "").strip()
    if recherche:
        services = services.filter(
            Q(nom__icontains=recherche) | Q(description__icontains=recherche)
        )
    services = [_attach_illustration(service) for service in services]

    return render(
        request,
        "services/list.html",
        {
            "title": "Services municipaux",
            "services": services,
            "total_services": total_services,
            "recherche": recherche,
        },
    )


def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects.prefetch_related("photos"), slug=slug, actif=True
    )
    _attach_illustration(service)
    return render(
        request,
        'services/detail.html',
        {'title': service.nom, 'service': service},
    )


@require_http_methods(["GET", "POST"])
def service_demande(request, slug):
    service = get_object_or_404(Service, slug=slug, actif=True)
    if request.method == "POST":
        form = DemandeServiceForm(request.POST, request.FILES)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.service = service
            if request.user.is_authenticated:
                demande.citoyen = request.user
            demande.save()
            return render(
                request,
                "services/demande_confirmation.html",
                {"title": "Demande envoyée", "demande": demande},
            )
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "nom_demandeur": request.user.get_full_name() or request.user.username,
                "email_demandeur": request.user.email,
                "telephone_demandeur": request.user.telephone,
            }
        form = DemandeServiceForm(initial=initial)

    return render(
        request,
        "services/demande_form.html",
        {"title": f"Demander : {service.nom}", "service": service, "form": form},
    )
