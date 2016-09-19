from django import forms
from . import models

class IngredientForm(forms.ModelForm):

    name = forms.CharField(max_length=30, 
                           widget=forms.TextInput(attrs={'class':'form-control',
                                                         'placeholder': "Food Item"}),
                           required=True,)
    amount = forms.FloatField(widget=forms.NumberInput(attrs={'class':'form-control',
                                                              'steps':'any',
                                                              'placeholder':'0'}),
                                                       required=True,)
    unit = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=models.Ingredient.UNIT)

    class Meta:
        model = models.Ingredient
        fields = ['name', 'amount', 'unit',]

class DishForm(forms.ModelForm): 

    name = forms.CharField(max_length=30,
                           widget=forms.TextInput(attrs={'placeholder': 'Dish', 'class': 'form-control'}),
                           required=True,)
    picture = forms.ImageField(required=False)
    recipe = forms.CharField(max_length=1000,
                             widget=forms.Textarea(attrs={'v-model': 'input', 'debounce': '300'}),
                             required=True)

    class Meta:
        model = models.Dish
        fields = ['name', 'picture', 'recipe',]
