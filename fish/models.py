from django.db import models
from aquariums.models import Aquarium


class FishSpecies(models.Model):
    name = models.CharField("Вид рыбы", max_length=150, unique=True)

    average_weight_grams = models.DecimalField(
        "Средний вес (г)",
        max_digits=6,
        decimal_places=2,
        help_text="Средний вес одной особи в граммах",
    )

    feeding_coefficient = models.DecimalField(
        "Коэффициент кормления",
        max_digits=6,
        decimal_places=3,
        help_text="Коэффициент для расчёта суточной нормы корма",
    )

    waste_factor = models.DecimalField(
        "Коэффициент загрязнения",
        max_digits=6,
        decimal_places=3,
        help_text="Относительный вклад вида в органическую нагрузку",
    )

    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Вид рыбы"
        verbose_name_plural = "Виды рыб"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AquariumFish(models.Model):
    aquarium = models.ForeignKey(
        Aquarium,
        on_delete=models.CASCADE,
        related_name="fish",
        verbose_name="Аквариум",
    )

    species = models.ForeignKey(
        FishSpecies,
        on_delete=models.PROTECT,
        related_name="aquarium_entries",
        verbose_name="Вид рыбы",
    )

    count = models.PositiveIntegerField("Количество", default=1)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Рыбы в аквариуме"
        verbose_name_plural = "Рыбы в аквариумах"
        constraints = [
            models.UniqueConstraint(
                fields=["aquarium", "species"],
                name="uniq_species_per_aquarium"
            )
        ]

    def __str__(self):
        return f"{self.aquarium.name}: {self.species.name} × {self.count}"