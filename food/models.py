from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=150, unique=True)
    protein_percent = models.DecimalField(max_digits=5, decimal_places=2)
    fat_percent = models.DecimalField(max_digits=5, decimal_places=2)
    fiber_percent = models.DecimalField(max_digits=5, decimal_places=2)
    ash_percent = models.DecimalField(max_digits=5, decimal_places=2)
    pollution_index = models.DecimalField(max_digits=6, decimal_places=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Food"
        ordering = ["name"]

    def __str__(self):
        return self.name