from django.shortcuts import render
from .models import FishSpecies

def fish_list(request):
    fish = FishSpecies.objects.filter(is_active=True)
    return render(request, "fish/fish_list.html", {"fish": fish})
