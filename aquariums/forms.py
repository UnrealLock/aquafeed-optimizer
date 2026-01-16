from django import forms
from .models import Aquarium
from fish.models import FishSpecies
from fish.models import AquariumFish
from .models import AquariumPlant

class AquariumCreateForm(forms.ModelForm):
    class Meta:
        model = Aquarium
        fields = [
            "name",
            "volume_liters",
            "temperature",
            "filtration_type",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "volume_liters": forms.NumberInput(attrs={"class": "form-control"}),
            "temperature": forms.NumberInput(attrs={"class": "form-control"}),
            "filtration_type": forms.Select(attrs={"class": "form-select"}),
        }

class AquariumFishForm(forms.ModelForm):
    class Meta:
        model = AquariumFish
        fields = ["species", "count"]

        widgets = {
            "species": forms.Select(attrs={"class": "form-select"}),
            "count": forms.NumberInput(attrs={"class": "form-control"}),
        }

class AquariumPlantForm(forms.ModelForm):
    class Meta:
        model = AquariumPlant
        fields = ["plant", "quantity"]

        widgets = {
            "plant": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }