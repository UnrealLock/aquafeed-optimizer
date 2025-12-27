from django.contrib import admin
from .models import FeedingPlan

@admin.register(FeedingPlan)
class FeedingPlanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "aquarium",
        "food",
        "daily_amount_grams",
        "feedings_per_day",
        "created_at",
    )

    list_filter = ("created_at", "feedings_per_day")
    search_fields = ("aquarium__name", "food__name", "aquarium__user__username")
    autocomplete_fields = ("aquarium", "food")