from django.urls import path

from . import views

app_name = "actualites"

urlpatterns = [
    path('', views.actualites_list, name='actualites_list'),
    path('<slug:slug>/', views.actualite_detail, name='actualite_detail'),
]
