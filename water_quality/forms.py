from django import forms
from .models import WaterChange

class WaterChangeForm(forms.ModelForm):
    class Meta:
        model = WaterChange
        fields = ['day_interval', 'percent']
        labels = {
            'day_interval': 'Интервал подмены (дней)',
            'percent': 'Процент подмены (%)',
        }
        help_texts = {
            'day_interval': 'Каждые N дней',
            'percent': 'Процент объёма воды для замены',
        }
        widgets = {
            'day_interval': forms.NumberInput(attrs={'class': 'form-control'}),
            'percent': forms.NumberInput(attrs={'class': 'form-control'}),
        }