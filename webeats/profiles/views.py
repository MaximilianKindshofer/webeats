from django.shortcuts import render, get_object_or_404, redirect
from meals.models import Dish
from .models import Favourite

def fav_toggle(request, pk):

    dish = get_object_or_404(Dish, pk=pk)
    if dish not in request.user.user_extend.get_favourites(): 
        Favourite.objects.create(user=request.user.user_extend,
                                 dish=dish)
    else:
        fav = Favourite.objects.filter(user=request.user.user_extend).get(dish=dish)
        fav.delete()
    return redirect('meals:dish_detail', dish.pk)
