from django.contrib import admin

from core.admin import GalerieInline

from .forms import LieuTouristiqueAdminForm
from .models import EvenementCulturel, LieuTouristique


@admin.register(LieuTouristique)
class LieuTouristiqueAdmin(admin.ModelAdmin):
    form = LieuTouristiqueAdminForm
    list_display = ("nom", "categorie", "commune", "publie")
    list_filter = ("categorie", "publie", "commune")
    search_fields = ("nom", "description", "adresse")
    prepopulated_fields = {"slug": ("nom",)}
    inlines = (GalerieInline,)


@admin.register(EvenementCulturel)
class EvenementCulturelAdmin(admin.ModelAdmin):
    list_display = ("titre", "lieu", "date_debut", "publie")
    list_filter = ("publie", "date_debut")
    search_fields = ("titre", "description")
    prepopulated_fields = {"slug": ("titre",)}
    inlines = (GalerieInline,)
