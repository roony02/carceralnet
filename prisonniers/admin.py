from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from datetime import date
from .models import Prisonnier


@admin.register(Prisonnier)
class PrisonnierAdmin(admin.ModelAdmin):

    list_display = (
        "photo_preview",
        "nom",
        "prenom",
        "cellule",
        "statut",
        "carte",
        "alerte_liberation",
    )

    search_fields = (
        "nom",
        "prenom",
        "numero_prisonnier",
        "cellule",
        "plaignant",
        "temoin",
    )

    readonly_fields = (
        "photo_preview",
        "carte",
    )

    fieldsets = (
        ("📷 Photo", {
            "fields": (
                "photo_preview",
                "photo",
            )
        }),

        ("👤 Informations", {
            "fields": (
                "numero_prisonnier",
                "nom",
                "postnom",
                "prenom",
                "nom_pere",
                "nom_mere",
                "nationalite",
                "etat_civil",
                "age",
            )
        }),

        ("⚖ Judiciaire", {
            "fields": (
                "plaignant",
                "temoin",
                "motif",
            )
        }),

        ("🏢 Pénitentiaire", {
            "fields": (
                "cellule",
                "date_entree",
                "date_sortie",
                "statut",
                "alarme_active",
            )
        }),

        ("🪪 Carte d'identité", {
            "fields": (
                "carte",
            )
        }),
    )

    class Media:
        js = ("prisonniers/alarme.js",)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="120" style="border-radius:8px;border:2px solid #2563eb;">',
                obj.photo.url,
            )
        return "Aucune photo"

    photo_preview.short_description = "Photo"

    def carte(self, obj):
        if obj.pk:
            url = reverse("carte_prisonnier", args=[obj.pk])
            return format_html(
                '<a class="button" href="{}" target="_blank" '
                'style="background:#0d6efd;color:white;padding:10px 18px;'
                'text-decoration:none;border-radius:6px;">'
                '🪪 Imprimer la carte'
                '</a>',
                url,
            )
        return "Enregistrez d'abord le prisonnier."

    carte.short_description = "Carte"

    def alerte_liberation(self, obj):
        if obj.alarme_active and obj.date_sortie == date.today():
            return format_html(
                '<span style="color:red;font-weight:bold;">'
                '🚨 LIBÉRATION AUJOURD’HUI'
                '</span>'
            )
        return "Aucune"

    alerte_liberation.short_description = "Alarme"