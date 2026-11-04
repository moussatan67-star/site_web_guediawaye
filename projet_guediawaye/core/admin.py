from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    Contact,
    FAQ,
    Newsletter,
    PageInstitutionnelle,
    PartenaireInstitutionnel,
    PhotoGalerie,
)


class GalerieInline(GenericTabularInline):
    model = PhotoGalerie
    extra = 1
    fields = ("image", "legende", "ordre")


@admin.register(PhotoGalerie)
class PhotoGalerieAdmin(admin.ModelAdmin):
    list_display = ("legende", "content_type", "object_id", "ordre")
    list_filter = ("content_type",)
    search_fields = ("legende",)


@admin.register(PageInstitutionnelle)
class PageInstitutionnelleAdmin(admin.ModelAdmin):
    list_display = ("titre", "type_page", "publiee", "ordre")
    list_filter = ("type_page", "publiee")
    search_fields = ("titre", "contenu")
    inlines = (GalerieInline,)


admin.site.register((Contact, FAQ, Newsletter, PartenaireInstitutionnel))
