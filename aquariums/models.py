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

class Plant(models.Model):
    name = models.CharField("Название растения", max_length=150, unique=True)

    nitrate_absorption = models.DecimalField(
        "Поглощение NO₃ (ppm/день)",
        max_digits=6,
        decimal_places=3,
    )

    phosphate_absorption = models.DecimalField(
        "Поглощение PO₄ (ppm/день)",
        max_digits=6,
        decimal_places=3,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Аквариумное растение"
        verbose_name_plural = "Аквариумные растения"

    def __str__(self):
        return self.name

class AquariumPlant(models.Model):
    aquarium = models.ForeignKey(
        Aquarium,
        on_delete=models.CASCADE,
        related_name="plants",
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.PROTECT,
        related_name="aquariums",
    )

    quantity = models.PositiveIntegerField("Количество", default=1)

    created_at = models.DateTimeField(auto_now_add=True)