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
        fields = ['name', 'nitrate_absorption', 'phosphate_absorption']

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    nitrate_absorption = forms.DecimalField(max_digits=6, decimal_places=3, widget=forms.NumberInput(attrs={"class": "form-control"}))
    phosphate_absorption = forms.DecimalField(max_digits=6, decimal_places=3, widget=forms.NumberInput(attrs={"class": "form-control"}))