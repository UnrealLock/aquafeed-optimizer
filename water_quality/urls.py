from django.urls import path
from . import views

app_name = "water_quality"

urlpatterns = [
    path("<int:aquarium_id>/add_water_change/", views.add_water_change, name="add_water_change"),
]