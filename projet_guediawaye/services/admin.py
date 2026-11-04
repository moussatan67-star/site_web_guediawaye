from django.contrib import admin

from core.admin import GalerieInline

from .models import DemandeService, Reclamation, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("nom", "actif")
    list_filter = ("actif",)
    search_fields = ("nom", "description")
    prepopulated_fields = {"slug": ("nom",)}
    inlines = (GalerieInline,)


@admin.register(DemandeService)
class DemandeServiceAdmin(admin.ModelAdmin):
    list_display = ("numero_dossier", "service", "nom_demandeur", "statut", "date_creation")
    list_filter = ("statut", "service", "date_creation")
    search_fields = ("numero_dossier", "nom_demandeur", "email_demandeur", "telephone_demandeur")
    readonly_fields = ("numero_dossier", "date_creation", "date_modification")


admin.site.register(Reclamation)
