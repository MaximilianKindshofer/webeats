from django import forms
from . import models

class IngredientForm(forms.Form):

    name = forms.CharField(max_length=30, 
                           widget=forms.TextInput(attrs={'placeholder': "Food Item"}),
                           required=True,)
    amount = forms.FloatField(widget=forms.NumberInput(attrs={'steps':'any', 'placeholder':'0'}),
                                                       required=True,)
    unit = forms.ChoiceField(widget=forms.Select, choices=models.Ingredients.UNIT)


class DishForm(forms.Form): 

    name = forms.CharField(max_length=30,
                           widget=forms.TextInput(attrs={'placeholder': 'Dish'}),
                           required=True,)
    picture = forms.ImageField()



