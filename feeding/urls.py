from django.urls import path
from . import views

app_name = "feeding"

urlpatterns = [
    path("plans/new/", views.feeding_plan_create, name="plan_create"),
    path("plans/<int:pk>/", views.feeding_plan_detail, name="plan_detail"),
]