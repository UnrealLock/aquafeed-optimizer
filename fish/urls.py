from django.urls import path
from .views import fish_list

urlpatterns = [
    path("", fish_list, name="fish_list"),
]