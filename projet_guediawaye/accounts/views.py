from django.shortcuts import render


def login_view(request):
    return render(request, 'accounts/login.html', {'title': 'Connexion'})


def profile_view(request):
    return render(request, 'accounts/profile.html', {'title': 'Profil'})
