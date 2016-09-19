from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from . import forms
from . import models
import random

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

@transaction.atomic
def seven_meals(request):

    count = models.Dish.objects.count()
    if count > 6:
        random_numbers = []
        while len(random_numbers) < 7:
            random_number = random.randrange(1,count+1)
            if random_number not in random_numbers:
                random_numbers.append(random_number)
    else:
        random_numbers = [random.randrange(1,count+1) for x in range(7)]
    dish = []
    for number in random_numbers:
        try:
            dish.append(models.Dish.objects.get(pk=number))
        except ObjectDoesNotExist:
            dish.append(models.Dish.objects.get(pk=random.randrange(1,count+1)))

    contex = {'meals': dish}
    return render(request, 'meals/7meals.html', contex)


def dish_update(request, pk):
    dish = get_object_or_404(models.Dish, pk=pk)
    IngredientFormset = modelformset_factory(models.Ingredient, form=forms.IngredientForm, fields=['name','amount','unit'])
    qset = dish.ingredient_set.all()
    ingredient_formset = IngredientFormset(queryset=qset)
    dish_form = forms.DishForm(instance=dish)
    
    context = {
        'dish_form': dish_form,
        'ingredient_formset': ingredient_formset,
         }
    return render(request, 'meals/add_dish.html', context)
