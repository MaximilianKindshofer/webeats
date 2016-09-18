from django.shortcuts import render
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from . import forms

@login_required
def add_dish(request):

    user = request.user
    IngredientFormset = formset_factory(forms.IngredientForm)

    if request.method == 'POST':
        dish_form = forms.DishForm(request.POST)
        ingredient_formset = forms.IngredientFormset(request.POST)
        
        if dish_form.is_valid() and ingredient_formset.is_valid():
            dish = Dish.objects.create(name=dish_form.cleaned_data.get('name'),
                                       picture=dish_form.cleaned_data.get('picture'))
        
        for ingredient in ingredient_formset:
            Ingredient.objects.create(name=ingredient.cleaned_data.get('name'),
                                      amount=ingredient.cleaned_data.get('amount'),
                                      unit=ingredient.cleaned_date.get('unit'),
                                      dish=dish)
    else:
        dish_form = forms.DishForm()
        ingredient_formset = IngredientFormset()

    context = {
        'dish_form': dish_form,
        'ingredient_formset': ingredient_formset,
    }

    return render(request, 'meals/add_dish.html', context)            
