from django.db import models


class Food(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)

    protein_percent = models.DecimalField(
        "Белок (%)",
        max_digits=5,
        decimal_places=2,
    )

    fat_percent = models.DecimalField(
        "Жиры (%)",
        max_digits=5,
        decimal_places=2,
    )

    fiber_percent = models.DecimalField(
        "Клетчатка (%)",
        max_digits=5,
        decimal_places=2,
    )

    ash_percent = models.DecimalField(
        "Зола (%)",
        max_digits=5,
        decimal_places=2,
    )

    pollution_index = models.DecimalField(
        "Индекс загрязнения",
        max_digits=6,
        decimal_places=3,
        help_text="Условный показатель, отражающий влияние корма на органическую нагрузку",
    )

    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Корм"
        verbose_name_plural = "Корма"
        ordering = ["name"]

    def __str__(self):
        return self.name