from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from feeding.forms import FeedingPlanCreateForm
from feeding.models import FeedingPlan
from feeding.services.plan_service import create_feeding_plan
from decimal import Decimal, ROUND_HALF_UP

@login_required
def feeding_plan_create(request):
    if request.method == "GET":
        form = FeedingPlanCreateForm(user=request.user)
        return render(request, "feeding/plan_form.html", {"form": form})
    
    form = FeedingPlanCreateForm(request.POST, user=request.user)

    if not form.is_valid():
        return render(request, "feeding/plan_form.html", {"form": form})
    
    aquarium = form.cleaned_data["aquarium"]
    food = form.cleaned_data["food"]
    feedings_per_day = form.cleaned_data["feedings_per_day"]

    try:
        plan = create_feeding_plan(
            aquarium=aquarium,
            food=food,
            feedings_per_day=feedings_per_day,
        )
    except ValueError as e:
        messages.error(request, str(e))
        return render(request, "feeding/plan_form.html", {"form": form})

    messages.success(request, "Feeding plan created.")
    return redirect("feeding:plan_detail", pk=plan.pk)

@login_required
def feeding_plan_detail(request, pk: int):
    plan = get_object_or_404(
        FeedingPlan.objects.select_related("aquarium", "food"),
        pk=pk,
        aquarium__user=request.user,
    )

    forecast = getattr(plan, "water_forecast", None)

    quant = Decimal("0.001")
    daily_amount_display = plan.daily_amount_grams.quantize(quant, rounding=ROUND_HALF_UP)
    per_feeding_display = (
    (plan.daily_amount_grams / Decimal(plan.feedings_per_day))
    .quantize(quant, rounding=ROUND_HALF_UP)
    )
    nitrate_display = phosphate_display = organic_display = None
    if forecast:
        nitrate_display = forecast.nitrate_ppm.quantize(quant, rounding=ROUND_HALF_UP)
        phosphate_display = forecast.phosphate_ppm.quantize(quant, rounding=ROUND_HALF_UP)
        organic_display = forecast.organic_load_index.quantize(quant, rounding=ROUND_HALF_UP)

    return render(
    request,
    "feeding/plan_detail.html",
    {
        "plan": plan,
        "forecast": forecast,
        "daily_amount_display": daily_amount_display,
        "per_feeding_display": per_feeding_display,
        "nitrate_display": nitrate_display,
        "phosphate_display": phosphate_display,
        "organic_display": organic_display,
    },
)