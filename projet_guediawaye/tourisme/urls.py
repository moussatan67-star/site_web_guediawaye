from django.urls import path

from . import views

app_name = "tourisme"

urlpatterns = [
    path('', views.tourisme_list, name='tourisme_list'),
    path('<slug:slug>/', views.tourisme_detail, name='tourisme_detail'),
]
