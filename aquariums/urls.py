from django.urls import path
from . import views

app_name = "aquariums"

urlpatterns = [
    path("", views.aquarium_list, name="list"),
]