from django.shortcuts import render
from .models import Food

def food_list(request):
    foods = Food.objects.filter(is_active=True)
    return render(request, "food/food_list.html", {"foods": foods})