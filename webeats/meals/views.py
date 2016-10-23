from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from . import forms
from . import models
import requests
import random
from profiles.secret import client_id

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

    count = models.Dish.objects.all().count()
    dish = []
    if count == 0:
        return render(request, 'meals/nomeals.html')
    try:
        fav_dish = request.user.user_extend.get_favourites()
    except ObjectDoesNotExist:
        fav_dish = []
    while len(dish) < 7:
        random_number = random.randrange(1, count+1)
        try:
            random_fav = random.randrange(0,len(fav_dish))
            dish.append(fav_dish[random_fav])
            del fav_dish[random_fav]
        except ValueError:
            try:
                dish.append(models.Dish.objects.get(pk=random_number))
            except models.Dish.DoesNotExist:
                pass

    contex = {'meals': dish}
    return render(request, 'meals/7meals.html', contex)

@login_required
def dish_update(request, pk):
    dish = get_object_or_404(models.Dish, pk=pk)
    dish_form = forms.DishForm(instance=dish)

    if request.POST:
        dish_form = forms.DishForm(request.POST)
        if dish_form.is_valid():
            dish_unsaved = dish_form.save(commit=False)
            dish.name = dish_unsaved.name
            dish.picture = dish_unsaved.picture
            dish.author = request.user
            dish.save()
            return redirect('meals:dish_detail', dish.pk)
        else:
            print(dish_form.errors)
    context = {
        'dish': dish,
        'dish_form': dish_form,
         }
    return render(request, 'meals/update_dish.html', context)


@login_required
def ingredient_update(request, pk):
    ingredient = get_object_or_404(models.Ingredient, pk=pk)
    ingredient_form = forms.IngredientForm(instance=ingredient)

    if request.POST:
        ingredient_form = forms.IngredientForm(request.POST)
        ingredient_unsaved = ingredient_form.save(commit=False)
        ingredient.name = ingredient_unsaved.name
        ingredient.amount = ingredient_unsaved.amount
        ingredient.unit = ingredient_unsaved.unit
        ingredient.save()
        return redirect('meals:dish_detail', ingredient.dish.pk)

    context = {'ingredient':ingredient, 'ingredient_form': ingredient_form}

    return render(request, 'meals/update_ingredient.html', context)

class DeleteIngredient(DeleteView):

    model = models.Ingredient
    def get_success_url(self):
        return reverse('meals:dish_detail', args=[self.object.dish.pk])
    


def get_groceries_dict(meal_pk_string):

    ingredients = []
    for pk in meal_pk_string:
        meal = models.Dish.objects.get(pk=pk)
        ingredients.append(meal.ingredient_set.all())
        groceries_dict = {} 
        for ingredient in ingredients:
            for item in ingredient:
                if item.name not in groceries_dict.keys(): 
                    groceries_dict[item.name] = item
                else:
                    dict_item = groceries_dict[item.name]
                    if dict_item.unit == item.unit:
                        groceries_dict[item.name].amount += item.amount
                    else:
                        groceries_dict["{} - {}".format(item.name, item.unit)] = item
    return groceries_dict

def wrap_up(request):
    if request.POST:
        meal_pk_string = request.POST.get('meals_pk', default=None)
        groceries_dict = get_groceries_dict(meal_pk_string)
        context = {
                'groceries': groceries_dict,
                'meal_pk_string': meal_pk_string,
                }
    return render(request, 'meals/wrap_up.html', context)

def to_wunderlist(request):

    if request.POST:
        meal_pk_string = request.POST.get('meals_pk', default=None)
        groceries_dict = get_groceries_dict(meal_pk_string)
    else:
        return redirect('index')

    headers = {'User-Agent': 'Webeats',
              'X-Access-Token': request.user.user_extend.wunderlist_token,
              'X-Client-ID': client_id,
              'Accept': 'application/json'}
    create_list_url = 'https://a.wunderlist.com/api/v1/lists'
    create_task_url = 'https://a.wunderlist.com/api/v1/tasks'
    create_list_data = {'title': 'Groceries'} 

    response = requests.post(create_list_url, headers=headers, data=create_list_data)
    if response.status == '201':
        list_response = response.json()
        list_id = list_response['id']

    for key, value in groceries_dict.items():
        create_task_data = {'list_id': list_id,
                            'title': "{} - {}".format(value.name, value.amount)
                            }
        response = requests.post(create_task_url, headers=headers, data=create_task)
    return redirect('index')
