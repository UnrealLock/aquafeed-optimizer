from django import forms
from .models import WaterChange

class WaterChangeForm(forms.ModelForm):
    class Meta:
        model = WaterChange
        fields = ['day_interval', 'percent']

    day_interval = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"}))
    percent = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={"class": "form-control"}))