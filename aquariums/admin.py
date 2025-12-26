from django.contrib import admin
from .models import Aquarium

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