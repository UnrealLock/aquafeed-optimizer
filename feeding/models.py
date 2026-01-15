from django.db import models
from aquariums.models import Aquarium
from food.models import Food


class FeedingPlan(models.Model):
    aquarium = models.ForeignKey(
        Aquarium,
        on_delete=models.CASCADE,
        related_name="feeding_plans",
        verbose_name="Аквариум",
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.PROTECT,
        related_name="feeding_plans",
        verbose_name="Корм",
    )

    daily_amount_grams = models.DecimalField(
        "Суточная норма (г)",
        max_digits=10,
        decimal_places=3,
        help_text="Общее количество корма в граммах на сутки",
    )

    feedings_per_day = models.PositiveSmallIntegerField(
        "Кормлений в день",
        default=2,
    )

    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "План кормления"
        verbose_name_plural = "Планы кормления"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.aquarium.name} — {self.food.name} ({self.daily_amount_grams} г/день)"