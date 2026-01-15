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
        fields = ["name", "nitrate_absorption", "phosphate_absorption"]
        labels = {
            "name": "Название растения",
            "nitrate_absorption": "Поглощение NO₃ (ppm/день)",
            "phosphate_absorption": "Поглощение PO₄ (ppm/день)",
        }
        help_texts = {
            "nitrate_absorption": "Сколько нитратов растение поглощает в сутки",
            "phosphate_absorption": "Сколько фосфатов растение поглощает в сутки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "nitrate_absorption": forms.NumberInput(attrs={"class": "form-control", "step": "0.001"}),
            "phosphate_absorption": forms.NumberInput(attrs={"class": "form-control", "step": "0.001"}),
        }