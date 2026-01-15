from django.db import models
from django.contrib.auth.models import User

class Aquarium(models.Model):
    FILTRATION_CHOICES = [
        ('internal', 'Внутренний фильтр'),
        ('external', 'Внешний фильтр'),
        ('sponge', 'Губчатый фильтр'),
        ('none', 'Без фильтрации'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='aquariums',
        verbose_name="Пользователь",
    )

    name = models.CharField("Название", max_length=100)
    volume_liters = models.PositiveIntegerField("Объём (л)")
    temperature = models.DecimalField(
        "Температура (°C)",
        max_digits=4,
        decimal_places=1,
        help_text="Температура воды в °C",
    )
    filtration_type = models.CharField(
        "Тип фильтрации",
        max_length=20,
        choices=FILTRATION_CHOICES,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Аквариум"
        verbose_name_plural = "Аквариумы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.volume_liters} л)"


class AquariumPlant(models.Model):
    aquarium = models.ForeignKey(
        Aquarium,
        on_delete=models.CASCADE,
        related_name="plants",
        verbose_name="Аквариум",
    )

    name = models.CharField("Название растения", max_length=100)

    nitrate_absorption = models.DecimalField(
        "Поглощение NO₃ (ppm/день)",
        max_digits=6,
        decimal_places=3,
        help_text="Сколько нитратов (NO₃) растение поглощает в сутки (ppm/день)",
    )

    phosphate_absorption = models.DecimalField(
        "Поглощение PO₄ (ppm/день)",
        max_digits=6,
        decimal_places=3,
        help_text="Сколько фосфатов (PO₄) растение поглощает в сутки (ppm/день)",
    )

    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Растение"
        verbose_name_plural = "Растения"

    def __str__(self):
        return self.name