from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from fish.models import AquariumFish
from water_quality.forms import WaterChangeForm
from water_quality.models import WaterChange

from .forms import AquariumCreateForm, AquariumFishForm, AquariumPlantForm
from .models import Aquarium, AquariumPlant


@login_required
def aquarium_list(request):
    aquariums = Aquarium.objects.filter(user=request.user)
    return render(request, "aquariums/list.html", {"aquariums": aquariums})


@login_required
def aquarium_create(request):
    if request.method == "POST":
        form = AquariumCreateForm(request.POST)
        if form.is_valid():
            aquarium = form.save(commit=False)
            aquarium.user = request.user
            aquarium.save()
            return redirect("aquariums:detail", pk=aquarium.pk)
    else:
        form = AquariumCreateForm()

    return render(request, "aquariums/create.html", {"form": form})


@login_required
def aquarium_detail(request, pk):
    aquarium = get_object_or_404(Aquarium, pk=pk, user=request.user)

    fish_list = AquariumFish.objects.select_related("species").filter(aquarium=aquarium)
    water_changes = WaterChange.objects.filter(aquarium=aquarium)
    plants = AquariumPlant.objects.filter(aquarium=aquarium)

    form = AquariumFishForm()
    water_change_form = WaterChangeForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "fish":
            form = AquariumFishForm(request.POST)
            if form.is_valid():
                species = form.cleaned_data["species"]
                count = form.cleaned_data["count"]

                with transaction.atomic():
                    entry, created = AquariumFish.objects.get_or_create(
                        aquarium=aquarium,
                        species=species,
                        defaults={"count": count},
                    )

                    if not created:
                        if count == 0:
                            entry.delete()
                        else:
                            entry.count = count
                            entry.save(update_fields=["count"])

                return redirect("aquariums:detail", pk=aquarium.pk)

        elif form_type == "water_change":
            water_change_form = WaterChangeForm(request.POST)
            if water_change_form.is_valid():
                day_interval = water_change_form.cleaned_data["day_interval"]
                percent = water_change_form.cleaned_data["percent"]

                with transaction.atomic():
                    existing = (
                        WaterChange.objects.filter(aquarium=aquarium).order_by("-id").first()
                    )
                    if existing:
                        WaterChange.objects.filter(aquarium=aquarium).exclude(pk=existing.pk).delete()
                        existing.day_interval = day_interval
                        existing.percent = percent
                        existing.save(update_fields=["day_interval", "percent"])
                    else:
                        WaterChange.objects.create(
                            aquarium=aquarium,
                            day_interval=day_interval,
                            percent=percent,
                        )

                return redirect("aquariums:detail", pk=aquarium.pk)

    return render(
        request,
        "aquariums/detail.html",
        {
            "aquarium": aquarium,
            "fish_list": fish_list,
            "water_changes": water_changes,
            "plants": plants,
            "form": form,
            "water_change_form": water_change_form,
        },
    )


@login_required
def aquarium_delete(request, pk: int):
    aquarium = get_object_or_404(Aquarium, pk=pk, user=request.user)

    if request.method == "POST":
        aquarium_name = aquarium.name
        aquarium.delete()
        messages.success(request, f'Aquarium "{aquarium_name}" deleted.')
        return redirect("aquariums:list")

    return render(request, "aquariums/confirm_delete.html", {"aquarium": aquarium})


@login_required
def add_plant(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, pk=aquarium_id, user=request.user)

    if request.method == "POST":
        form = AquariumPlantForm(request.POST)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.aquarium = aquarium
            plant.save()
            return redirect("aquariums:detail", pk=aquarium.pk)
    else:
        form = AquariumPlantForm()

    return render(request, "aquariums/add_plant.html", {"form": form, "aquarium": aquarium})