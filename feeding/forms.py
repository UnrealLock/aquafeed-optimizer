from django import forms
from aquariums.models import Aquarium
from food.models import Food

class FeedingPlanCreateForm(forms.Form):
    aquarium = forms.ModelChoiceField(
        queryset=Aquarium.objects.none(),
        label="Аквариум",
    )
    
    food = forms.ModelChoiceField(
        queryset=Food.objects.all(),
        label="Корм",
    )
    
    feedings_per_day = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=2,
        label="Кормлений в день",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user is not None:
            self.fields["aquarium"].queryset = Aquarium.objects.filter(user=user)