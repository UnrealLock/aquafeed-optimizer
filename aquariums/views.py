from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aquarium
from .forms import AquariumCreateForm
from .forms import AquariumFishForm
from fish.models import AquariumFish
from django.db import transaction

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

    if request.method == "POST":
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
    else:
        form = AquariumFishForm()

    return render(
        request,
        "aquariums/detail.html",
        {"aquarium": aquarium, "fish_list": fish_list, "form": form},
    )