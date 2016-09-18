from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

@login_required
def add_dish(request):

    user = request.user
    IngredientFormset = formset_factory(forms.IngredientForm)

    if request.method == 'POST':
        dish_form = forms.DishForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormset(request.POST)
        
        if dish_form.is_valid() and ingredient_formset.is_valid():
            dish = models.Dish(name=dish_form.cleaned_data.get('name'),
                        author=request.user,
                        recipe=dish_form.cleaned_data.get('recipe'),
                        picture=dish_form.cleaned_data.get('picture')
                        )
            dish.save()
        
            for ingredient in ingredient_formset:
                models.Ingredient.objects.create(name=ingredient.cleaned_data.get('name'),
                                          amount=ingredient.cleaned_data.get('amount'),
                                          unit=ingredient.cleaned_data.get('unit'),
                                          dish=dish)
            return redirect('meals:dish_detail', dish.pk)
    else:
        dish_form = forms.DishForm()
        ingredient_formset = IngredientFormset()

    context = {
        'dish_form': dish_form,
        'ingredient_formset': ingredient_formset,
    }

    return render(request, 'meals/add_dish.html', context)


def dish_detail(request, pk):
    
    dish = get_object_or_404(models.Dish, pk=pk)
    context = {'dish': dish}
    return render(request, 'meals/dish.html', context)
