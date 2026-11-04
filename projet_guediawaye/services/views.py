from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import DemandeServiceForm
from .models import Service

def services_list(request):
    services = Service.objects.filter(actif=True)
    return render(
        request,
        'services/list.html',
        {'title': 'Services', 'services': services},
    )


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, actif=True)
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
