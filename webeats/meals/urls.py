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
]

