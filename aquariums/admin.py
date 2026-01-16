from django.contrib import admin
from .models import Aquarium, Plant, AquariumPlant

@admin.register(Aquarium)
class AquariumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'user',
        'volume_liters',
        'temperature',
        'filtration_type',
        'created_at',
    )
    list_filter = ('filtration_type', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "nitrate_absorption", "phosphate_absorption")
    search_fields = ("name",)

@admin.register(AquariumPlant)
class AquariumPlantAdmin(admin.ModelAdmin):
    list_display = ("aquarium", "plant", "quantity")
    autocomplete_fields = ("aquarium", "plant")