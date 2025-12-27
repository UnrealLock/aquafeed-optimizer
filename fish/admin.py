from django.contrib import admin
from .models import FishSpecies, AquariumFish

@admin.register(FishSpecies)
class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "average_weight_grams",
        "feeding_coefficient",
        "waste_factor",
        "is_active",
        "created_at",
    )

    list_filter = ("is_active", "created_at")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(AquariumFish)
class AquariumFishAdmin(admin.ModelAdmin):
    list_display = ("id", "aquarium", "species", "count", "created_at")
    list_filter = ("created_at", "species")
    search_fields = ("aquarium__name", "species__name", "aquarium__user__username")
    autocomplete_fields = ("aquarium", "species")