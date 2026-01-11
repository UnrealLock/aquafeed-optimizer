from decimal import Decimal
from django.db import transaction
from fish.models import AquariumFish
from water_quality.models import WaterQualityForecast
from water_quality.models import WaterChange
from aquariums.models import AquariumPlant

FILTRATION_EFFICIENCY = {
    "external": Decimal("1.00"),
    "internal": Decimal("0.80"),
    "sponge": Decimal("0.70"),
    "none": Decimal("0.40"),
}

def build_daily_forecast(feeding_plan, days: int = 30) -> list[dict]:
    aquarium = feeding_plan.aquarium
    food = feeding_plan.food

    daily_food = feeding_plan.daily_amount_grams
    volume = Decimal(aquarium.volume_liters)

    fish_entries = AquariumFish.objects.select_related("species").filter(
        aquarium=aquarium
    )

    total_waste_factor = sum(
        Decimal(e.count) * e.species.waste_factor for e in fish_entries
    )

    eff = FILTRATION_EFFICIENCY.get(
        aquarium.filtration_type, Decimal("0.7")
    )

    pollution = food.pollution_index

    daily_no3_inc = (daily_food * pollution * Decimal("10.0")) / volume
    daily_po4_inc = (daily_food * pollution * Decimal("2.0")) / volume
    daily_organic_inc = (daily_food * (Decimal("1.0") + total_waste_factor)) / eff

    plants = AquariumPlant.objects.filter(aquarium=aquarium)
    plant_no3_abs = sum(p.nitrate_absorption for p in plants)
    plant_po4_abs = sum(p.phosphate_absorption for p in plants)

    water_changes = WaterChange.objects.filter(aquarium=aquarium)

    no3 = po4 = organic = Decimal("0")
    rows = []

    for day in range(1, days + 1):
        no3 += daily_no3_inc
        po4 += daily_po4_inc
        organic += daily_organic_inc

        no3 = max(Decimal("0"), no3 - plant_no3_abs)
        po4 = max(Decimal("0"), po4 - plant_po4_abs)

        for wc in water_changes:
            if day % wc.day_interval == 0:
                factor = (Decimal("100") - wc.percent) / Decimal("100")
                no3 *= factor
                po4 *= factor
                organic *= factor

        rows.append({
            "day": day,
            "no3": float(no3.quantize(Decimal("0.001"))),
            "po4": float(po4.quantize(Decimal("0.001"))),
            "organic": float(organic.quantize(Decimal("0.001"))),
        })

    return rows

@transaction.atomic
def create_or_update_forecast(feeding_plan) -> WaterQualityForecast:
    aquarium = feeding_plan.aquarium
    food = feeding_plan.food

    daily_food = feeding_plan.daily_amount_grams
    volume = Decimal(aquarium.volume_liters)

    if volume <= 0:
        raise ValueError("Aquarium volume must be > 0 liters")
    
    fish_entries = AquariumFish.objects.select_related("species").filter(aquarium=aquarium)
    
    total_waste_factor = Decimal("0")
    for e in fish_entries:
        total_waste_factor += Decimal(e.count) * e.species.waste_factor

    eff = FILTRATION_EFFICIENCY.get(aquarium.filtration_type, Decimal("0.70"))

    organic_load_index = (daily_food * (Decimal("1.0") + total_waste_factor)) / eff

    pollution = food.pollution_index

    nitrate_ppm = (daily_food * pollution * Decimal("10.0")) / volume
    phosphate_ppm = (daily_food * pollution * Decimal("2.0")) / volume

    forecast, _created = WaterQualityForecast.objects.update_or_create(
        feeding_plan=feeding_plan,
        defaults={
            "nitrate_ppm": nitrate_ppm,
            "phosphate_ppm": phosphate_ppm,
            "organic_load_index": organic_load_index,
        },
    )

    return forecast