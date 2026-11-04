from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path('', views.services_list, name='services_list'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
    path('<slug:slug>/demander/', views.service_demande, name='service_demande'),
]
