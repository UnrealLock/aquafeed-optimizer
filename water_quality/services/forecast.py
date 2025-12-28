from decimal import Decimal
from django.db import transaction
from fish.models import AquariumFish
from water_quality.models import WaterQualityForecast

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

    total_waste_factor = Decimal("0")
    for e in fish_entries:
        total_waste_factor += Decimal(e.count) * e.species.waste_factor

    eff = FILTRATION_EFFICIENCY.get(
        aquarium.filtration_type, Decimal("0.70")
    )

    pollution = food.pollution_index

    no3 = Decimal("0")
    po4 = Decimal("0")
    organic = Decimal("0")

    rows = []

    for day in range(1, days + 1):
        daily_no3 = (daily_food * pollution * Decimal("10.0")) / volume
        daily_po4 = (daily_food * pollution * Decimal("2.0")) / volume
        daily_organic = (daily_food * (Decimal("1.0") + total_waste_factor)) / eff

        no3 += daily_no3
        po4 += daily_po4
        organic += daily_organic

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