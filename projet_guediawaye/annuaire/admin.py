from django.contrib import admin

from core.admin import GalerieInline

from .models import EntrepriseAnnuaire


@admin.register(EntrepriseAnnuaire)
class EntrepriseAnnuaireAdmin(admin.ModelAdmin):
    list_display = ("nom", "secteur", "commune", "valide")
    list_filter = ("secteur", "commune", "valide")
    search_fields = ("nom", "description", "adresse")
    prepopulated_fields = {"slug": ("nom",)}
    inlines = (GalerieInline,)
