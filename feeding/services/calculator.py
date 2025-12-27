from decimal import Decimal
from fish.models import AquariumFish

def calculate_daily_amount_grams(aquarium) -> Decimal:
    total = Decimal("0")
    entries = AquariumFish.objects.select_related("species").filter(aquarium=aquarium)
    for entry in entries:
        total += (
            Decimal(entry.count)
            * entry.species.average_weight_grams
            * entry.species.feeding_coefficient
        )
    
    return total