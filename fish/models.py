from django.db import models
from aquariums.models import Aquarium

class FishSpecies(models.Model):
    name = models.CharField(max_length=150, unique=True)
    average_weight_grams = models.DecimalField(max_digits=6, decimal_places=2)
    feeding_coefficient = models.DecimalField(max_digits=6, decimal_places=3)
    waste_factor = models.DecimalField(max_digits=6, decimal_places=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fish species"
        verbose_name_plural = "Fish species"
        ordering = ["name"]
    
    def __str__(self):
        return self.name

class AquariumFish(models.Model):
    aquarium = models.ForeignKey(
        Aquarium,
        on_delete=models.CASCADE,
        related_name="fish"
    )

    species = models.ForeignKey(
        FishSpecies,
        on_delete=models.PROTECT,
        related_name="aquarium_entries"
    )

    count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aquarium fish"
        verbose_name_plural = "Aquarium fish"
        constraints = [
            models.UniqueConstraint(
                fields=["aquarium", "species"],
                name="uniq_species_per_aquarium"
            )
        ]
    
    def __str__(self):
        return f"{self.aquarium.name}: {self.species.name} x{self.count}"