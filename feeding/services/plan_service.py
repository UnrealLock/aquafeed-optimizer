from decimal import Decimal
from django.db import transaction
from aquariums.models import Aquarium
from food.models import Food
from feeding.models import FeedingPlan
from feeding.services.calculator import calculate_daily_amount_grams

@transaction.atomic
def create_feeding_plan(
    *,
    aquarium: Aquarium,
    food: Food,
    feedings_per_day: int = 2,
) -> FeedingPlan:
    daily_amount = calculate_daily_amount_grams(aquarium)
    if daily_amount <= Decimal("0"):
        raise ValueError("Daily feeding amount is zero. Aquarium has no fish.")
    
    feeding_plan = FeedingPlan.objects.create(
        aquarium=aquarium,
        food=food,
        daily_amount_grams=daily_amount,
        feedings_per_day=feedings_per_day,
    )

    from water_quality.services import create_or_update_forecast
    create_or_update_forecast(feeding_plan)

    return feeding_plan

