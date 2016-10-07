from django.conf.urls import url
from . import views
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
    url(r'^ingredient/(?P<pk>[\d]+)/update/$',
        views.ingredient_update,
        name='ingredient_update',),
    url(r'^meals/wrap_up/$',
        views.wrap_up,
        name='wrap_up',),
]

