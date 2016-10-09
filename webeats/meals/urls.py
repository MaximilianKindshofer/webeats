from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from . import views
from .models import Dish, Ingredient
urlpatterns = [
    url(r'^add_dish/$',
        views.add_dish,
        name='add_dish',),
    url(r'^dish/(?P<pk>[\d]+)/detail/$',
        views.dish_detail,
        name='dish_detail',),
    url(r'^meals/$',
        views.seven_meals,
        name='seven_meals'),
    url(r'^dish/(?P<pk>[\d]+)/update/$',
        views.dish_update,
        name='dish_update',),
    url(r'^dish/(?P<pk>[\d]+)/delete/$',
        DeleteView.as_view(
            model=Dish,
            success_url=reverse_lazy('index')
        ),
        name='dish_delete',),
    url(r'^ingredient/(?P<pk>[\d]+)/update/$',
        views.ingredient_update,
        name='ingredient_update',),
    url(r'^ingredient/(?P<pk>[\d]+)/delete/$',
        views.DeleteIngredient.as_view(),
        name='ingredient_delete'),
    url(r'^meals/wrap_up/$',
        views.wrap_up,
        name='wrap_up',),
]

