from django.urls import path
from . import views
from water_quality import views as water_views

app_name = "aquariums"

urlpatterns = [
    path("", views.aquarium_list, name="list"),
    path("new/", views.aquarium_create, name="create"),
    path("<int:pk>/", views.aquarium_detail, name="detail"),
    path("<int:pk>/delete/", views.aquarium_delete, name="delete"),
    path("<int:pk>/", views.aquarium_detail, name="detail"),
    path(
        "<int:aquarium_id>/add_water_change/",
        water_views.add_water_change,
        name="add_water_change"
    ),
    path(
    "<int:aquarium_id>/add_plant/",
    views.add_plant,
    name="add_plant",
    ),
    path(
    "plant/<int:pk>/delete/",
    views.delete_plant,
    name="delete_plant",
    ),
]