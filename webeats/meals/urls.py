from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^add_dish/$',
        views.add_dish,
        name='add_dish',),
]

