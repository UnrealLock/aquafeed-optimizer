from django.contrib import admin
from .models import Food

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "protein_percent",
        "fat_percent",
        "fiber_percent",
        "ash_percent",
        "pollution_index",
        "is_active",
        "created_at",
    )

    list_filter = ("is_active", "created_at")
    search_fields = ("name",)