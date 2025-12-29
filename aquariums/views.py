from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Aquarium

@login_required
def aquarium_list(request):
    aquariums = Aquarium.objects.filter(user=request.user)
    return render(request, "aquariums/list.html", {"aquariums": aquariums})
