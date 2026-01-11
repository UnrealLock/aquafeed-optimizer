from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import WaterChange
from .forms import WaterChangeForm
from aquariums.models import Aquarium

def add_water_change(request, aquarium_id):
    aquarium = get_object_or_404(Aquarium, pk=aquarium_id, user=request.user)

    if request.method == "POST":
        form = WaterChangeForm(request.POST)
        if form.is_valid():
            water_change = form.save(commit=False)
            water_change.aquarium = aquarium
            water_change.save()
            return redirect('aquariums:detail', pk=aquarium.pk)
    else:
        form = WaterChangeForm()

    return render(request, 'water_quality/add_water_change.html', {'form': form, 'aquarium': aquarium})
