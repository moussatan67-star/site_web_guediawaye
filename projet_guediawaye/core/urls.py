from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('commune/<slug:slug>/', views.page_institutionnelle, name='page_institutionnelle'),
]
