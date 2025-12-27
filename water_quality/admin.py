from django.contrib import admin
from .models import WaterQualityForecast

@admin.register(WaterQualityForecast)
class WaterQualityForecastAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "feeding_plan",
        "nitrate_ppm",
        "phosphate_ppm",
        "organic_load_index",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = (
        "feeding_plan__aquarium__name",
        "feeding_plan__aquarium__user__username",
        "feeding_plan__food__name",
    )

    autocomplete_fields = ("feeding_plan",)