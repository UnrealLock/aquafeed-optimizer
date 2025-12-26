from django.db import models
from django.contrib.auth.models import User

class Aquarium(models.Model):
    FILTRATION_CHOICES = [
        ('internal', 'Internal filter'),
        ('external', 'External filter'),
        ('sponge', 'Sponge filter'),
        ('none', 'No filtration'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='aquariums'
    )

    name = models.CharField(max_length=100)
    volume_liters = models.PositiveIntegerField()
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text="Temperature in °C"
    )
    filtration_type = models.CharField(
        max_length=20,
        choices=FILTRATION_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aquarium"
        verbose_name_plural = "Aquariums"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.volume_liters} L)"