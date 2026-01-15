from django.db import models
from feeding.models import FeedingPlan
from aquariums.models import Aquarium


class WaterQualityForecast(models.Model):
    feeding_plan = models.OneToOneField(
        FeedingPlan,
        on_delete=models.CASCADE,
        related_name="water_forecast",
        verbose_name="План кормления",
    )

    nitrate_ppm = models.DecimalField(
        "Нитраты NO₃ (ppm)",
        max_digits=10,
        decimal_places=3,
    )

    phosphate_ppm = models.DecimalField(
        "Фосфаты PO₄ (ppm)",
        max_digits=10,
        decimal_places=3,
    )

    organic_load_index = models.DecimalField(
        "Индекс органической нагрузки",
        max_digits=10,
        decimal_places=3,
    )

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Прогноз качества воды"
        verbose_name_plural = "Прогнозы качества воды"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Прогноз для плана кормления #{self.feeding_plan_id}"


class WaterChange(models.Model):
    aquarium = models.OneToOneField(
        Aquarium,
        on_delete=models.CASCADE,
        related_name="water_change",
        verbose_name="Аквариум",
    )

    day_interval = models.PositiveSmallIntegerField(
        "Интервал (дней)",
        help_text="Каждые N дней",
    )

    percent = models.DecimalField(
        "Процент подмены (%)",
        max_digits=5,
        decimal_places=2,
        help_text="Процент объёма воды, который меняется за одну подмену",
    )

    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Подмена воды"
        verbose_name_plural = "Подмены воды"

    def __str__(self):
        return f"{self.percent}% каждые {self.day_interval} дн."