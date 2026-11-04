from django.urls import path

from . import views

app_name = "annuaire"

urlpatterns = [
    path('', views.annuaire_list, name='annuaire_list'),
    path('<slug:slug>/', views.entreprise_detail, name='entreprise_detail'),
]
