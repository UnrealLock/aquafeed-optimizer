from django.urls import path
from .views import food_list

urlpatterns = [
    path("", food_list, name="food_list"),
]