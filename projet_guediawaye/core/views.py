from django.contrib import messages
from django.shortcuts import redirect, render

from actualites.models import Actualite

from .forms import ContactForm


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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Votre message a bien été envoyé. La mairie pourra le consulter.",
            )
            return redirect('core:contact')
    else:
        form = ContactForm()

    return render(
        request,
        'core/contact.html',
        {'title': 'Contact', 'form': form},
    )
