# -*- coding: utf-8 -*-

from decimal import Decimal
from fish.models import FishSpecies
from food.models import Food
from aquariums.models import Plant

fish_data = [
    ("Гуппи (Guppy)", "0.30", "0.8", "0.20"),
    ("Неон (Neon tetra)", "0.25", "0.7", "0.18"),
    ("Скалярия (Angelfish)", "3.00", "1.2", "0.50"),
    ("Анцитрус (Ancistrus)", "5.00", "1.0", "0.80"),
    ("Моллинезия (Molly)", "1.20", "0.9", "0.35"),
]

for name, weight, feed, waste in fish_data:
    FishSpecies.objects.get_or_create(
        name=name,
        defaults={
            "average_weight_grams": Decimal(weight),
            "feeding_coefficient": Decimal(feed),
            "waste_factor": Decimal(waste),
        },
    )

plant_data = [
    ("Анубиас (Anubias)", "0.020", "0.003"),
    ("Валлиснерия (Vallisneria)", "0.080", "0.012"),
    ("Элодея (Elodea)", "0.120", "0.018"),
    ("Роголистник (Hornwort)", "0.150", "0.020"),
    ("Яванский папоротник (Java Fern)", "0.035", "0.005"),
]

for name, no3, po4 in plant_data:
    Plant.objects.get_or_create(
        name=name,
        defaults={
            "nitrate_absorption": Decimal(no3),
            "phosphate_absorption": Decimal(po4),
        },
    )

food_data = [
    ("TetraMin (TetraMin)", 47, 10, 2, 8, "1.00"),
    ("Sera Vipagran (Vipagran)", 45, 8, 3, 7, "1.10"),
    ("Hikari Cichlid Gold (Hikari)", 48, 9, 2, 6, "1.30"),
    ("JBL NovoGranomix (JBL)", 46, 8, 2, 7, "1.05"),
    ("AquaMenu Универсал (AquaMenu)", 42, 7, 4, 9, "0.95"),
]

for name, protein, fat, fiber, ash, pollution in food_data:
    Food.objects.get_or_create(
        name=name,
        defaults={
            "protein_percent": protein,
            "fat_percent": fat,
            "fiber_percent": fiber,
            "ash_percent": ash,
            "pollution_index": Decimal(pollution),
        },
    )

print("Seed data added.")