from django.db import models
from feeding.models import FeedingPlan

class WaterQualityForecast(models.Model):
    feeding_plan = models.OneToOneField(
        FeedingPlan,
        on_delete=models.CASCADE,
        related_name="water_forecast",
    )

    nitrate_ppm = models.DecimalField(max_digits=10, decimal_places=3)
    phosphate_ppm = models.DecimalField(max_digits=10, decimal_places=3)
    organic_load_index = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Water quality forecast"
        verbose_name_plural = "Water quality forecasts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Forecast for plan #{self.feeding_plan_id}"