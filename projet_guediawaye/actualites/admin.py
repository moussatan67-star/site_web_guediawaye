from django.contrib import admin

from core.admin import GalerieInline

from .models import Actualite


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ("titre", "categorie", "statut", "date_publication")
    list_filter = ("categorie", "statut")
    search_fields = ("titre", "contenu")
    prepopulated_fields = {"slug": ("titre",)}
    inlines = (GalerieInline,)
