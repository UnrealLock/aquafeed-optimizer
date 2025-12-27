from django.db import models
from aquariums.models import Aquarium
from food.models import Food

class FeedingPlan(models.Model):
    aquarium = models.ForeignKey(
        Aquarium,
        on_delete=models.CASCADE,
        related_name="feeding_plans"
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.PROTECT,
        related_name="feeding_plans"
    )

    daily_amount_grams = models.DecimalField(max_digits=10, decimal_places=3)
    feedings_per_day = models.PositiveSmallIntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feeding plan"
        verbose_name_plural = "Feeding plans"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.aquarium.name} - {self.food.name} ({self.daily_amount_grams} g/day)"