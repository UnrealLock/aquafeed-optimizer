from django.urls import path
from . import views

app_name = "aquariums"

urlpatterns = [
    path("", views.aquarium_list, name="list"),
    path("new/", views.aquarium_create, name="create"),
    path("<int:pk>/", views.aquarium_detail, name="detail"),
]